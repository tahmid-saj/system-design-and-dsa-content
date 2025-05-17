Note: Most of the times, it is suitable to have pre-signed URLs to upload blobs directly to the blob store:

Presigned URLs are a feature provided by cloud storage services, such as Amazon S3, that allow temporary access to private resources. These URLs are generated with a specific expiration time, after which they become invalid, offering a secure way to share files without altering permissions. When a presigned URL is created, it includes authentication information as part of the query string, enabling controlled access to otherwise private objects.

This makes them ideal for use cases like temporary file sharing, uploading objects to a bucket without giving users full API access, or providing limited-time access to resources. Presigned URLs can be generated programmatically using the cloud provider's SDK, allowing developers to integrate this functionality into applications seamlessly. This method enhances security by ensuring that sensitive data remains protected while still being accessible to authorized users for a limited period.

# Uploading file and binary data using HTTP

When uploading a file using HTTP, the request usually uses the POST or PUT method with the Content-Type header set to multipart/form-data (most common) or another appropriate MIME type. Below is an example of how the full HTTP request headers and body look when uploading a file.

## Example: File Upload Request (Multipart/Form-Data)

Request headers:

```http
POST /upload HTTP/1.1
Content-Type: multipart/form-data; boundary=---------------------------123456789012345678901234
Content-Length: 3456
```

Request body:

```plaintext
-----------------------------123456789012345678901234
Content-Disposition: form-data; name="file"; filename="example.txt"
Content-Type: text/plain

<file contents go here>
-----------------------------123456789012345678901234
Content-Disposition: form-data; name="description"

This is an example text file.
-----------------------------123456789012345678901234--
```

- Boundary
  - The boundary string separates the different parts of the request body. It is defined in the Content-Type header.

- Form Data
  - File Part
    - Includes Content-Disposition (with name and filename) and Content-Type headers, followed by the file content.
  - Text Part
    - Includes Content-Disposition for form field description and its value.

## Example: File Upload Request (Raw Binary Upload)

In some cases (e.g., APIs that accept direct file uploads), the file content is sent raw in the request body.

Request headers:

```http
POST /upload HTTP/1.1
Content-Type: text/plain
Content-Length: 1234
```

Request body:

```plaintext
<file contents go here>
```

- Content-Type
  - Specifies the type of the file being uploaded (text/plain, application/json, etc.).
- Body
  - Contains only the file's raw data.

## Example: JSON Metadata + File Upload (Hybrid Approach)

Some APIs use a combination of JSON and file data for file uploads.

Request headers:

```http
POST /upload HTTP/1.1
Content-Type: multipart/form-data; boundary=---------------------------123456789012345678901234
```

Request body:

```plaintext
-----------------------------123456789012345678901234
Content-Disposition: form-data; name="metadata"
Content-Type: application/json

{
  "fileName": "example.txt",
  "description": "This is an example text file."
}
-----------------------------123456789012345678901234
Content-Disposition: form-data; name="file"; filename="example.txt"
Content-Type: text/plain

<file contents go here>
-----------------------------123456789012345678901234--
```

## Key notes

- Content-Type Header
  - Use multipart/form-data when uploading a file alongside form fields or metadata.
  - Use the file's MIME type (text/plain, image/png, etc.) if sending raw data.

- Boundary
  - The boundary in multipart/form-data separates parts of the body.
  - Ensure the same boundary is used in the Content-Type header and the body.

- Encoding
  - File content is sent as-is unless otherwise required (e.g., base64 encoding for specific APIs).

# Downloading file and binary data using HTTP

When downloading a file using HTTP, the server responds to a GET or POST request with the file's content, headers, and metadata. Here's how the full HTTP request and response might look.

## HTTP Request for File Download

Request headers:

```http
GET /files/example.txt HTTP/1.1
Accept: application/octet-stream
```

- GET
  - The standard method for downloading files.
- Accept
  - Specifies the file type expected by the client (application/octet-stream for binary files or a specific MIME type like image/jpeg).

## HTTP Response for File Download

Response headers:

```http
HTTP/1.1 200 OK
Content-Type: application/octet-stream
Content-Disposition: attachment; filename="example.txt"
Content-Length: 12345
Cache-Control: no-cache
ETag: "abc123"
```

Response body:

```plaintext
<binary or text content of the file>
```

- Content-Type
  - Indicates the file's MIME type (application/octet-stream for generic binary files, or a specific type like image/png).
- Content-Disposition
  - If attachment, the browser will prompt the user to download the file.
  - The filename attribute suggests the file name for saving.
- Content-Length
  - Specifies the size of the file (in bytes).
- Cache-Control
  - Helps manage caching (e.g., no-cache forces re-fetching every time).
- ETag
  - A unique identifier for the file version, useful for caching.

## Handling Partial File Downloads

For resuming downloads, the client can request specific byte ranges.

Request headers:

```http
GET /files/example.txt HTTP/1.1
Range: bytes=500-999
```

Response headers:

```http
HTTP/1.1 206 Partial Content
Content-Type: application/octet-stream
Content-Range: bytes 500-999/12345
Content-Length: 500
```

- Range
  - Specifies the part of the file the client needs (500-999 in this case).
- 206 Partial Content
  - Indicates the response contains only part of the file.
- Content-Range
  - Confirms the byte range returned (500-999) and the total file size (12345).

## Downloading via POST Request

Sometimes, downloading files requires a POST request (e.g., generating reports on the fly or using APIs).

Request:

```http
POST /files/download HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json
Accept: application/pdf

{
  "fileId": "1234",
  "format": "pdf"
}
```

Response:

```http
HTTP/1.1 200 OK
Content-Type: application/pdf
Content-Disposition: attachment; filename="report.pdf"
Content-Length: 67890
```

- The response body contains the binary content of the generated file.

## Streaming File Downloads

For large files, servers may stream content in chunks to the client.

Response with chunked encoding:

```http
HTTP/1.1 200 OK
Content-Type: application/octet-stream
Transfer-Encoding: chunked
Content-Disposition: attachment; filename="largefile.zip"

4
Data
6
Chunked
0
```

- Transfer-Encoding
  - chunked Indicates the file is sent in chunks without specifying Content-Length.
- Each chunk starts with its size (in hexadecimal), followed by the content.

## Common headers for file downloads

- Content-Type
  - Describes the file type (e.g., application/pdf, image/png).
- Content-Disposition
  - Suggests whether the file should be displayed inline (inline) or downloaded (attachment) and provides the file name.
- Content-Length
  - Provides the file's total size (optional for chunked responses).
- ETag
  - Helps with caching and validation.
- Cache-Control
  - Manages how clients and proxies cache the file.



