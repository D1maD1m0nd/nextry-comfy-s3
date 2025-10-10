# 📊 Workflow Diagram - Webhook Sender Node

## 🔄 Data Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         ComfyUI Workflow                                │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│   Load Image     │
│   or Generate    │
└────────┬─────────┘
         │
         │ IMAGE
         ▼
┌──────────────────┐
│ Image Processing │
│  (Optional)      │
└────────┬─────────┘
         │
         │ IMAGE
         ▼
┌──────────────────────────────┐
│  Nextry Save Image to S3     │
│  ┌────────────────────────┐  │
│  │ • Saves preview.webp   │  │
│  │ • Saves stock.png      │  │
│  │ • Returns S3 paths     │  │
│  └────────────────────────┘  │
└──────┬──────────────┬────────┘
       │              │
       │ preview_path │ stock_path
       │ (STRING)     │ (STRING)
       │              │
       ▼              ▼
┌─────────────────────────────────────┐
│   Nextry Webhook Sender             │
│  ┌──────────────────────────────┐   │
│  │ INPUT:                       │   │
│  │ • endpoint (STRING)          │   │
│  │ • preview_image (STRING)     │   │
│  │ • stock_image (STRING)       │   │
│  └──────────────────────────────┘   │
│                                      │
│  ┌──────────────────────────────┐   │
│  │ PROCESS:                     │   │
│  │ 1. Validate inputs           │   │
│  │ 2. Prepare JSON payload      │   │
│  │ 3. Send POST request         │   │
│  │ 4. Handle response/errors    │   │
│  │ 5. Return status             │   │
│  └──────────────────────────────┘   │
│                                      │
│  ┌──────────────────────────────┐   │
│  │ OUTPUT:                      │   │
│  │ • webhook_response (STRING)  │   │
│  │   JSON with status & data    │   │
│  └──────────────────────────────┘   │
└──────────────┬──────────────────────┘
               │
               │ HTTP POST
               ▼
┌─────────────────────────────────────┐
│   Your Backend Server               │
│   http://localhost:8000/...         │
│  ┌──────────────────────────────┐   │
│  │ RECEIVES:                    │   │
│  │ {                            │   │
│  │   "preview_image": "s3://...",  │
│  │   "stock_image": "s3://..."  │   │
│  │ }                            │   │
│  └──────────────────────────────┘   │
│                                      │
│  ┌──────────────────────────────┐   │
│  │ ACTIONS:                     │   │
│  │ • Download from S3           │   │
│  │ • Process images             │   │
│  │ • Store in database          │   │
│  │ • Trigger workflows          │   │
│  │ • Send notifications         │   │
│  └──────────────────────────────┘   │
│                                      │
│  ┌──────────────────────────────┐   │
│  │ RESPONDS:                    │   │
│  │ {                            │   │
│  │   "status": "success",       │   │
│  │   "message": "..."           │   │
│  │ }                            │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
```

---

## 🔀 Alternative Workflows

### Option 1: Multiple Image Processing

```
[Generate Image 1] ─→ [Save S3] ─┐
                                  │
[Generate Image 2] ─→ [Save S3] ─┼─→ [Webhook Sender]
                                  │     ↓
[Generate Image 3] ─→ [Save S3] ─┘   [Backend]
```

### Option 2: Batch Processing

```
[Batch Generator]
      ↓
[For Each Image]
      ↓
[Save to S3]
      ↓
[Webhook Sender] ─→ [Backend Process]
```

### Option 3: Conditional Webhook

```
[Generate Image]
      ↓
[Quality Check]
      ↓
   [Pass?]
    ↙  ↘
  Yes   No
   ↓     ↓
[Save]  [Reject]
   ↓
[Webhook]
   ↓
[Backend]
```

---

## 📡 HTTP Request Details

### Request Format

```http
POST /generation/comfy_webhook HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "preview_image": "s3://my-bucket/output/preview_abc123.webp",
  "stock_image": "s3://my-bucket/output/stock_abc123.png"
}
```

### Success Response

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "message": "Images received and processed"
}
```

### Error Response

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "status": "error",
  "message": "Invalid image paths"
}
```

---

## 🎯 Node Execution Flow

```
┌─────────────────────────────────────┐
│  1. Node receives inputs            │
│     • endpoint                      │
│     • preview_image                 │
│     • stock_image                   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  2. Validate inputs                 │
│     • Check endpoint format         │
│     • Check image paths             │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  3. Prepare payload                 │
│     payload = {                     │
│       "preview_image": ...,         │
│       "stock_image": ...            │
│     }                               │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  4. Send HTTP POST request          │
│     • Set Content-Type: JSON        │
│     • Set timeout: 30 seconds       │
│     • Wait for response             │
└──────────────┬──────────────────────┘
               │
        ┌──────┴──────┐
        │             │
     Success       Error
        │             │
        ▼             ▼
┌──────────┐    ┌──────────┐
│ Parse    │    │ Handle   │
│ Response │    │ Error    │
└────┬─────┘    └────┬─────┘
     │               │
     └───────┬───────┘
             │
             ▼
┌─────────────────────────────────────┐
│  5. Return result                   │
│     {                               │
│       "success": true/false,        │
│       "status_code": ...,           │
│       "response": {...}             │
│     }                               │
└─────────────────────────────────────┘
```

---

## 🔍 Error Handling Flow

```
┌─────────────────────┐
│  Send HTTP Request  │
└──────────┬──────────┘
           │
    ┌──────┴──────────────────────────┐
    │                                  │
    ▼                                  ▼
┌────────┐                      ┌──────────┐
│Success?│                      │ Timeout? │
└───┬────┘                      └─────┬────┘
    │Yes                              │Yes
    ▼                                 ▼
┌─────────────┐               ┌──────────────┐
│ Return 200  │               │ Return Error │
│ + Response  │               │ "timeout"    │
└─────────────┘               └──────────────┘
                                     │
                              ┌──────┴──────┐
                              │             │
                              ▼             ▼
                        ┌──────────┐  ┌──────────┐
                        │ Network  │  │ Unknown  │
                        │ Error    │  │ Error    │
                        └──────────┘  └──────────┘
                              │             │
                              └──────┬──────┘
                                     │
                                     ▼
                              ┌──────────────┐
                              │ Log & Return │
                              │ Error Details│
                              └──────────────┘
```

---

## 🎨 Use Case: Complete Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    Complete Image Generation Pipeline            │
└─────────────────────────────────────────────────────────────────┘

[User Request] → [ComfyUI API]
                      ↓
              [Generate Image]
                      ↓
              [Apply Effects]
                      ↓
              [Save to S3]
                      ↓
            [Webhook Sender] ─────→ [Backend API]
                                           ↓
                                    [Download from S3]
                                           ↓
                                    [Post-processing]
                                           ↓
                                    [Save to Database]
                                           ↓
                                    [Update UI/Notify User]
                                           ↓
                                    [Analytics & Logging]

Timeline:
─────────────────────────────────────────────────────────────────
0s        5s       10s      15s      20s      25s      30s
│         │        │        │        │        │        │
Generate  Save     Webhook  Download Process  Save     Done
          to S3    Sent     Images   Images   to DB    ✓
```

---

## 🚀 Integration Patterns

### Pattern 1: Immediate Processing

```
ComfyUI → Webhook → Backend
                      ↓
                   Process
                      ↓
                    Response
```

### Pattern 2: Async Queue

```
ComfyUI → Webhook → Backend
                      ↓
                   Add to Queue
                      ↓
                   Response (202 Accepted)
                      
                   [Later...]
                   Worker picks up task
                      ↓
                   Process
```

### Pattern 3: Event-Driven

```
ComfyUI → Webhook → Event Bus
                      ↓
          ┌──────────┼──────────┐
          ▼          ▼          ▼
      Service A  Service B  Service C
      (Process)  (Store)    (Notify)
```

---

## 📊 Monitoring & Logging

```
┌─────────────────────────────────────┐
│  ComfyUI Console                    │
│  ┌───────────────────────────────┐  │
│  │ INFO: Webhook request to...   │  │
│  │ INFO: Preview: s3://...        │  │
│  │ INFO: Stock: s3://...          │  │
│  │ INFO: Status code: 200         │  │
│  │ INFO: Response: {...}          │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  Backend Server Logs                │
│  ┌───────────────────────────────┐  │
│  │ [POST] /generation/webhook    │  │
│  │ Received: preview, stock      │  │
│  │ Processing images...          │  │
│  │ Success! Sent 200 OK          │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

---

## 🎯 Best Practices

1. **Always validate inputs** before sending
2. **Handle all error cases** gracefully
3. **Log everything** for debugging
4. **Use appropriate timeouts** (default: 30s)
5. **Implement retry logic** on backend if needed
6. **Monitor webhook deliveries** in production
7. **Use HTTPS** in production environments
8. **Validate webhook signatures** for security

---

**Note:** This diagram represents the default workflow. You can customize it based on your specific needs!

