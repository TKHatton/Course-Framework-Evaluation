// netlify/functions/upload-files.js
const { createClient } = require('@supabase/supabase-js');
const formidable = require('formidable');

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
    console.log('Processing file upload...');
    
    // Parse the multipart form data
    const files = await parseMultipartForm(event);
    
    if (!files || files.length === 0) {
      throw new Error('No files received');
    }
    
    console.log(`Processing ${files.length} files`);
    
    // Upload files to Supabase Storage
    const uploadedFilePaths = [];
    const originalFilenames = [];
    
    for (const file of files) {
      const fileName = `${Date.now()}-${file.name}`;
      
      console.log(`Uploading file: ${file.name} (${file.size} bytes)`);
      
      const { data, error } = await supabase.storage
        .from('course-submissions')
        .upload(fileName, file.buffer, {
          contentType: file.type,
          upsert: false
        });
      
      if (error) {
        console.error('Upload error for', file.name, ':', error);
        throw new Error(`Failed to upload ${file.name}: ${error.message}`);
      }
      
      uploadedFilePaths.push(data.path);
      originalFilenames.push(file.name);
      console.log(`Successfully uploaded: ${file.name}`);
    }
    
    // Create submission record in database
    console.log('Creating submission record...');
    const { data: submission, error: submissionError } = await supabase
      .from('course_submissions')
      .insert([{
        file_paths: uploadedFilePaths,
        original_filenames: originalFilenames,
        submission_status: 'uploaded',
        analysis_status: 'pending',
        created_at: new Date().toISOString()
      }])
      .select()
      .single();
    
    if (submissionError) {
      console.error('Submission creation error:', submissionError);
      throw new Error(`Failed to create submission record: ${submissionError.message}`);
    }
    
    console.log('Submission created successfully:', submission.id);
    
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        submission: submission,
        filesUploaded: uploadedFilePaths.length,
        message: `Successfully uploaded ${uploadedFilePaths.length} files`
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

async function parseMultipartForm(event) {
  try {
    // Convert base64 body to buffer for binary file data
    const body = event.isBase64Encoded 
      ? Buffer.from(event.body, 'base64')
      : Buffer.from(event.body);
    
    // For Netlify functions, we need to parse the multipart data manually
    // This is a simplified parser - for production, you might want a more robust solution
    
    const boundary = getBoundary(event.headers['content-type'] || event.headers['Content-Type']);
    if (!boundary) {
      throw new Error('No boundary found in content-type');
    }
    
    const parts = parseMultipartData(body, boundary);
    const files = [];
    
    for (const part of parts) {
      if (part.filename) {
        files.push({
          name: part.filename,
          type: part.contentType || 'application/octet-stream',
          size: part.data.length,
          buffer: part.data
        });
      }
    }
    
    return files;
    
  } catch (error) {
    console.error('Error parsing multipart form:', error);
    throw new Error('Failed to parse uploaded files');
  }
}

function getBoundary(contentType) {
  const match = contentType.match(/boundary=(.+)$/);
  return match ? match[1] : null;
}

function parseMultipartData(buffer, boundary) {
  const parts = [];
  const boundaryBuffer = Buffer.from(`--${boundary}`);
  const endBoundaryBuffer = Buffer.from(`--${boundary}--`);
  
  let start = 0;
  let end = buffer.indexOf(boundaryBuffer, start);
  
  while (end !== -1) {
    if (start > 0) {
      // Parse this part
      const partBuffer = buffer.slice(start, end);
      const part = parsePart(partBuffer);
      if (part) {
        parts.push(part);
      }
    }
    
    start = end + boundaryBuffer.length;
    end = buffer.indexOf(boundaryBuffer, start);
  }
  
  return parts;
}

function parsePart(partBuffer) {
  try {
    // Find the double CRLF that separates headers from data
    const headerEnd = partBuffer.indexOf('\r\n\r\n');
    if (headerEnd === -1) return null;
    
    const headerSection = partBuffer.slice(0, headerEnd).toString();
    const dataSection = partBuffer.slice(headerEnd + 4);
    
    // Parse headers
    const headers = {};
    const headerLines = headerSection.split('\r\n');
    
    for (const line of headerLines) {
      if (line.includes(':')) {
        const [key, value] = line.split(':', 2);
        headers[key.trim().toLowerCase()] = value.trim();
      }
    }
    
    // Extract filename and content type from Content-Disposition header
    const disposition = headers['content-disposition'];
    if (!disposition) return null;
    
    const filenameMatch = disposition.match(/filename="([^"]+)"/);
    const nameMatch = disposition.match(/name="([^"]+)"/);
    
    if (!filenameMatch && !nameMatch) return null;
    
    return {
      name: nameMatch ? nameMatch[1] : null,
      filename: filenameMatch ? filenameMatch[1] : null,
      contentType: headers['content-type'],
      data: dataSection.slice(0, -2) // Remove trailing CRLF
    };
    
  } catch (error) {
    console.error('Error parsing part:', error);
    return null;
  }
}