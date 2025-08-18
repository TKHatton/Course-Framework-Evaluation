// netlify/functions/upload-files.js
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
    console.log('Processing file upload...');
    
    // Parse the incoming data
    const contentType = event.headers['content-type'] || '';
    
    if (contentType.includes('application/json')) {
      // Handle base64 file data from the frontend
      const { fileName, fileContent, fileType } = JSON.parse(event.body);
      
      if (!fileName || !fileContent) {
        throw new Error('Missing file data');
      }

      console.log(`Processing file: ${fileName}, type: ${fileType}`);

      // Extract text content based on file type
      let textContent = '';
      
      try {
        if (fileType === 'text/plain' || fileName.endsWith('.txt')) {
          // Handle plain text files
          const buffer = Buffer.from(fileContent, 'base64');
          textContent = buffer.toString('utf-8');
        } 
        else if (fileType === 'application/pdf' || fileName.endsWith('.pdf')) {
          // For PDFs, we'll need to extract text (simplified approach)
          textContent = 'PDF content extraction not yet implemented. Please convert to text format.';
        }
        else if (fileType.includes('text/') || fileName.endsWith('.docx')) {
          // Handle other text-based files
          const buffer = Buffer.from(fileContent, 'base64');
          textContent = buffer.toString('utf-8');
        }
        else {
          textContent = `Unsupported file type: ${fileType}. Please upload text files, PDFs, or Word documents.`;
        }
        
        console.log(`Extracted text content length: ${textContent.length}`);
        
      } catch (extractError) {
        console.error('Text extraction error:', extractError);
        textContent = 'Error extracting text from file. Please try a different format.';
      }

      // Create submission record
      const submission = {
        file_name: fileName,
        file_type: fileType,
        text_content: textContent.substring(0, 10000), // Limit to 10k chars
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

      console.log('Submission created:', submissionData.id);

      // Now call the analysis function with the actual content
      const analysisResponse = await fetch(`${process.env.URL}/.netlify/functions/analyze-course`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text_content: textContent,
          submission_id: submissionData.id
        })
      });

      if (!analysisResponse.ok) {
        console.error('Analysis request failed:', analysisResponse.status);
        // Return basic submission data if analysis fails
        return {
          statusCode: 200,
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            success: true,
            submission: submissionData,
            analysis_results: [{
              title: 'Analysis Unavailable',
              category: 'System Error',
              alignment_score: 0,
              analysis: 'Unable to complete analysis due to technical issues.',
              recommendations: ['Please try again later'],
              evidence: ['Analysis service temporarily unavailable']
            }]
          })
        };
      }

      const analysisData = await analysisResponse.json();
      console.log('Analysis completed');

      return {
        statusCode: 200,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          success: true,
          submission: submissionData,
          analysis_results: analysisData.results
        })
      };

    } else {
      throw new Error('Unsupported content type');
    }

  } catch (error) {
    console.error('Upload error:', error);
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        error: 'Upload failed',
        message: error.message,
        analysis_results: [{
          title: 'Upload Error',
          category: 'System Error',
          alignment_score: 0,
          analysis: 'Failed to process uploaded file.',
          recommendations: ['Check file format and try again', 'Ensure file contains text content'],
          evidence: ['File upload or processing error']
        }]
      })
    };
  }
};