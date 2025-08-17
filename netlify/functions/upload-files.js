// netlify/functions/upload-files.js
const { createClient } = require('@supabase/supabase-js');

// Environment variables (set in Netlify dashboard)
const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_KEY
);

exports.handler = async (event, context) => {
  // Enable CORS
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS'
  };

  // Handle preflight requests
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
    console.log('Upload function started');
    console.log('Content-Type:', event.headers['content-type']);
    
    // For now, let's create a test submission without actual file parsing
    // This will help us debug the function deployment
    
    const testSubmission = {
      file_paths: ['test-file-path.pdf'],
      original_filenames: ['test-upload.pdf'],
      submission_status: 'uploaded',
      analysis_status: 'pending',
      created_at: new Date().toISOString()
    };
    
    console.log('Creating test submission...');
    
    // Create submission record in database
    const { data: submission, error: submissionError } = await supabase
      .from('course_submissions')
      .insert([testSubmission])
      .select()
      .single();
    
    if (submissionError) {
      console.error('Submission creation error:', submissionError);
      throw new Error(`Failed to create submission: ${submissionError.message}`);
    }
    
    console.log('Test submission created:', submission.id);
    
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        submission: submission,
        filesUploaded: 1,
        message: 'Test upload successful - function is working!'
      })
    };
    
  } catch (error) {
    console.error('Upload function error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ 
        success: false,
        error: 'Upload failed', 
        details: error.message 
      })
    };
  }
};