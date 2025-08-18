// netlify/functions/analyze-course.js
const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY
);

exports.handler = async (event, context) => {
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const { text_content, submission_id } = JSON.parse(event.body);
    
    if (!text_content || text_content.trim().length < 50) {
      return {
        statusCode: 200,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          results: [{
            title: 'Insufficient Content for Analysis',
            category: 'Content Review',
            alignment_score: 0,
            analysis: 'The submitted content does not contain enough educational material to perform a meaningful framework analysis. Please ensure your submission includes substantial course content such as lesson plans, curriculum outlines, or educational materials.',
            recommendations: [
              'Submit course syllabi, lesson plans, or curriculum documents',
              'Include learning objectives and assessment methods',
              'Provide content that demonstrates educational structure and methodology'
            ],
            evidence: ['Content too brief for educational analysis']
          }]
        })
      };
    }

    // Check if content is actually educational
    const educationalKeywords = [
      'learn', 'student', 'curriculum', 'lesson', 'objective', 'assessment', 'education',
      'teaching', 'course', 'syllabus', 'assignment', 'exam', 'grade', 'classroom',
      'instructor', 'pedagogy', 'study', 'academic', 'training', 'module', 'unit'
    ];

    const contentLower = text_content.toLowerCase();
    const educationalMatches = educationalKeywords.filter(keyword => 
      contentLower.includes(keyword)
    );

    // If less than 3 educational keywords found, likely not educational content
    if (educationalMatches.length < 3) {
      return {
        statusCode: 200,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          results: [{
            title: 'Non-Educational Content Detected',
            category: 'Content Classification',
            alignment_score: 0,
            analysis: 'The submitted content does not appear to be educational material. Our framework is designed to evaluate courses, curricula, lesson plans, and other educational content.',
            recommendations: [
              'Submit educational materials such as course syllabi or lesson plans',
              'Include learning objectives and educational methodologies',
              'Ensure content relates to teaching, learning, or curriculum design'
            ],
            evidence: [`Found only ${educationalMatches.length} educational indicators in content`]
          }]
        })
      };
    }

    // Now do actual framework analysis using your vectorized framework
    console.log('Analyzing educational content with', educationalMatches.length, 'educational indicators');

    // Generate embeddings for the submitted content
    const embeddingResponse = await fetch('https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.HUGGINGFACE_API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        inputs: text_content.substring(0, 1000) // Limit to first 1000 chars for embedding
      })
    });

    if (!embeddingResponse.ok) {
      throw new Error('Failed to generate embeddings');
    }

    const embedding = await embeddingResponse.json();
    
    // Search your vectorized framework using the embedding
    const { data: matches, error } = await supabase.rpc('match_framework_chunks_hf', {
      query_embedding: embedding,
      match_threshold: 0.3, // Lower threshold = more matches
      match_count: 8
    });

    if (error) {
      console.error('Supabase RPC error:', error);
      throw new Error('Framework matching failed');
    }

    console.log('Found', matches?.length || 0, 'framework matches');

    // Convert matches to analysis results
    const results = [];
    const processedCategories = new Set();

    if (matches && matches.length > 0) {
      matches.forEach((match, index) => {
        // Skip if similarity is too low
        if (match.similarity < 0.4) return;
        
        // Create category from content or use default
        const category = match.metadata?.category || `Framework Area ${index + 1}`;
        
        // Avoid duplicate categories
        if (processedCategories.has(category)) return;
        processedCategories.add(category);

        const alignmentScore = Math.round(match.similarity * 100);
        
        results.push({
          title: `${category} Analysis`,
          category: category,
          alignment_score: alignmentScore,
          analysis: `Your content shows ${alignmentScore}% alignment with this framework area. ${match.content.substring(0, 200)}...`,
          recommendations: generateRecommendations(alignmentScore, category),
          evidence: [
            `Framework match: ${match.similarity.toFixed(2)} similarity`,
            `Content analysis: ${educationalMatches.length} educational indicators found`
          ]
        });
      });
    }

    // If no good matches, provide honest feedback
    if (results.length === 0) {
      results.push({
        title: 'Limited Framework Alignment',
        category: 'Overall Assessment',
        alignment_score: 15,
        analysis: 'Your submitted content appears to be educational but shows limited alignment with the SHE IS AI framework principles. This could indicate either different pedagogical approaches or content that would benefit from framework integration.',
        recommendations: [
          'Review the SHE IS AI framework principles for alignment opportunities',
          'Consider incorporating equity-centered design principles',
          'Explore inclusive teaching methodologies',
          'Assess current curriculum for bias and exclusion patterns'
        ],
        evidence: [
          `Educational content detected (${educationalMatches.length} indicators)`,
          'Framework alignment below threshold for specific recommendations'
        ]
      });
    }

    // Save analysis results to database
    if (submission_id) {
      await supabase.from('analysis_results').insert({
        submission_id: submission_id,
        results: results,
        analysis_type: 'framework_alignment',
        created_at: new Date().toISOString()
      });
    }

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ results })
    };

  } catch (error) {
    console.error('Analysis error:', error);
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        error: 'Analysis failed',
        results: [{
          title: 'Analysis Error',
          category: 'System Error',
          alignment_score: 0,
          analysis: 'Unable to complete framework analysis due to technical issues. Please try again.',
          recommendations: ['Try uploading your content again', 'Ensure file contains educational material'],
          evidence: ['System error during analysis']
        }]
      })
    };
  }
};

function generateRecommendations(score, category) {
  const baseRecommendations = {
    'Equity & Inclusion': [
      'Incorporate diverse perspectives and voices',
      'Review content for bias and exclusionary language',
      'Ensure accessibility for all learning differences'
    ],
    'Learning Structure': [
      'Implement clear learning objectives',
      'Design scaffolded learning experiences',
      'Include multiple assessment formats'
    ],
    'Assessment': [
      'Use authentic, real-world assessments',
      'Provide multiple ways to demonstrate learning',
      'Include self and peer reflection opportunities'
    ]
  };

  const recommendations = baseRecommendations[category] || [
    'Align content with framework principles',
    'Incorporate equity-centered design',
    'Review for inclusive practices'
  ];

  if (score < 40) {
    return [
      'Significant alignment improvements needed',
      ...recommendations
    ];
  } else if (score < 70) {
    return [
      'Good foundation with room for enhancement',
      ...recommendations
    ];
  } else {
    return [
      'Strong framework alignment detected',
      'Consider deeper integration of advanced principles',
      ...recommendations.slice(1)
    ];
  }
}