# ⚡ Severless Functions


## Examples of all Requests data

> If you pass data into an Appwrite Function, it'll be found in the request object. This includes all invocation inputs from Appwrite SDKs, HTTP calls, Appwrite events, or browsers visiting the configured domain. Explore the request object with the following function, which logs all request params to the Appwrite Console

```python
import json

def main(context):
    context.log(context.req.body_raw)            # Raw request body, contains request data
    context.log(json.dumps(context.req.body))    # Object from parsed JSON request body, otherwise string
    context.log(json.dumps(context.req.headers)) # String key-value pairs of all request headers, keys are lowercase
    context.log(context.req.scheme)              # Value of the x-forwarded-proto header, usually http or https
    context.log(context.req.method)              # Request method, such as GET, POST, PUT, DELETE, PATCH, etc.
    context.log(context.req.url)                 # Full URL, for example: http://awesome.appwrite.io:8000/v1/hooks?limit=12&offset=50
    context.log(context.req.host)                # Hostname from the host header, such as awesome.appwrite.io
    context.log(context.req.port)                # Port from the host header, for example 8000
    context.log(context.req.path)                # Path part of URL, for example /v1/hooks
    context.log(context.req.query_string)        # Raw query params string. For example "limit=12&offset=50"
    context.log(json.dumps(context.req.query))   # Parsed query params. For example, req.query.limit

    return context.res.send("All the request parameters are logged to the Appwrite Console.")
```

### GET /

- Returns a "Hello, World!" message.

**Response**

Sample `200` Response:

```text
Hello, World!
```

### POST, PUT, PATCH, DELETE /

- Returns a "Learn More" JSON response.

**Response**

Sample `200` Response:

```json
{
  "motto": "Build like a team of hundreds_",
  "learn": "https://appwrite.io/docs",
  "connect": "https://appwrite.io/discord",
  "getInspired": "https://builtwith.appwrite.io"
}
```

## ⚙️ Configuration

| Setting           | Value                             |
|-------------------|-----------------------------------|
| Runtime           | Python (3.9)                      |
| Entrypoint        | `src/main.py`                     |
| Build Commands    | `pip install -r requirements.txt` |
| Permissions       | `any`                             |
| Timeout (Seconds) | 15 (60 for queryPriceHistory)     |

## 🔒 Environment Variables

No environment variables required.
