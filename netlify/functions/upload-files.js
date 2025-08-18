// netlify/functions/upload-files.js
const { createClient } = require('@supabase/supabase-js');

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY
);

exports.handler = async (event, context) => {
  // Add CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Content-Type': 'application/json'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    console.log('Processing upload request...');
    
    const { fileName, fileContent, fileType } = JSON.parse(event.body);
    
    if (!fileName || !fileContent) {
      throw new Error('Missing file data');
    }

    console.log(`Processing file: ${fileName}`);

    // Extract text content from base64
    let textContent = '';
    
    try {
      const buffer = Buffer.from(fileContent, 'base64');
      textContent = buffer.toString('utf-8');
      
      // Clean up the text content
      textContent = textContent.replace(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]/g, '');
      
      console.log(`Extracted ${textContent.length} characters`);
      
    } catch (extractError) {
      console.error('Text extraction error:', extractError);
      textContent = `Error extracting text from ${fileName}`;
    }

    // Create submission record
    const submission = {
      file_name: fileName,
      file_type: fileType,
      text_content: textContent.substring(0, 5000), // Limit to 5k chars
      status: 'uploaded',
      created_at: new Date().toISOString()
    };

    const { data: submissionData, error: submissionError } = await supabase
      .from('course_submissions')
      .insert([submission])
      .select()
      .single();

    if (submissionError) {
      console.error('Submission error:', submissionError);
      throw new Error('Failed to create submission record');
    }

    console.log('Submission created successfully');

    // Now analyze the content directly here
    const analysisResults = await analyzeContent(textContent);

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        submission: submissionData,
        analysis_results: analysisResults
      })
    };

  } catch (error) {
    console.error('Upload error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        error: 'Upload processing failed',
        message: error.message,
        analysis_results: [{
          title: 'Upload Error',
          category: 'System Error',
          alignment_score: 0,
          analysis: 'Failed to process uploaded file.',
          recommendations: ['Check file format and try again'],
          evidence: ['File processing error']
        }]
      })
    };
  }
};

// Simple content analysis function
async function analyzeContent(textContent) {
  console.log('Starting content analysis...');
  
  if (!textContent || textContent.trim().length < 50) {
    return [{
      title: 'Insufficient Content',
      category: 'Content Review',
      alignment_score: 0,
      analysis: 'The submitted content does not contain enough text for analysis.',
      recommendations: ['Submit files with substantial educational content'],
      evidence: ['Content too brief for analysis']
    }];
  }

  // Check for educational keywords
  const educationalKeywords = [
    'learn', 'student', 'curriculum', 'lesson', 'objective', 'assessment', 'education',
    'teaching', 'course', 'syllabus', 'assignment', 'exam', 'grade', 'classroom',
    'instructor', 'pedagogy', 'study', 'academic', 'training', 'module', 'unit',
    'workshop', 'seminar', 'lecture', 'tutorial', 'evaluation', 'feedback'
  ];

  const contentLower = textContent.toLowerCase();
  const educationalMatches = educationalKeywords.filter(keyword => 
    contentLower.includes(keyword)
  );

  console.log(`Found ${educationalMatches.length} educational indicators`);

  // If very few educational keywords, reject as non-educational
  if (educationalMatches.length < 3) {
    return [{
      title: 'Non-Educational Content Detected',
      category: 'Content Classification',
      alignment_score: 0,
      analysis: 'The submitted content does not appear to be educational material. Our framework evaluates courses, curricula, lesson plans, and other educational content.',
      recommendations: [
        'Submit educational materials such as course syllabi or lesson plans',
        'Include learning objectives and educational methodologies',
        'Ensure content relates to teaching, learning, or curriculum design'
      ],
      evidence: [
        `Found only ${educationalMatches.length} educational indicators`,
        'Content does not match educational material patterns'
      ]
    }];
  }

  // If educational content detected, provide framework analysis
  const frameworkKeywords = {
    'equity': ['equity', 'inclusion', 'diverse', 'bias', 'fair', 'accessible'],
    'assessment': ['assess', 'evaluate', 'portfolio', 'feedback', 'rubric'],
    'community': ['community', 'collaboration', 'peer', 'group', 'social'],
    'accessibility': ['accessible', 'accommodation', 'universal', 'inclusive']
  };

  const results = [];
  
  Object.entries(frameworkKeywords).forEach(([area, keywords]) => {
    const matches = keywords.filter(keyword => contentLower.includes(keyword));
    const score = Math.min(90, (matches.length * 20) + Math.random() * 30);
    
    if (matches.length > 0) {
      results.push({
        title: `${area.charAt(0).toUpperCase() + area.slice(1)} Framework Analysis`,
        category: area,
        alignment_score: Math.round(score),
        analysis: `Your content shows some alignment with ${area} principles. Found references to: ${matches.join(', ')}.`,
        recommendations: [
          `Strengthen ${area} integration throughout the curriculum`,
          'Consider adding more explicit framework alignment',
          'Review content for deeper integration opportunities'
        ],
        evidence: [
          `Educational indicators: ${educationalMatches.length}`,
          `${area} keywords found: ${matches.length}`
        ]
      });
    }
  });

  // If no framework matches, provide basic educational feedback
  if (results.length === 0) {
    results.push({
      title: 'Basic Educational Content',
      category: 'General Assessment',
      alignment_score: 25,
      analysis: 'Your content appears to be educational but shows limited alignment with our equity-centered framework.',
      recommendations: [
        'Review the SHE IS AI framework for alignment opportunities',
        'Consider incorporating equity and inclusion principles',
        'Add explicit learning objectives and assessment strategies'
      ],
      evidence: [
        `Educational content detected (${educationalMatches.length} indicators)`,
        'Limited framework-specific content found'
      ]
    });
  }

  return results;
}