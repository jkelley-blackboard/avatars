Copilot Provided this addtional information - I haven't tested it exactly.
Below is a clear, end‑to‑end walkthrough with copy‑pasteable cURL, the required entitlements, and common pitfalls.

***

## Overview of the flow

1.  **Upload the image file**  
    `POST /learn/api/public/v1/uploads` → returns an **uploadId**. You’ll use this ID to reference the file in subsequent requests. [\[docs.anthology.com\]](https://docs.anthology.com/docs/blackboard/rest-apis/advanced/ultra-assignments), [\[blackboard.github.io\]](https://blackboard.github.io/rest-apis/learn/advanced/ultra-assignments)

2.  **Update the user to point at that upload**  
    `PATCH /learn/api/public/v1/users/{userId}` with an `avatar` object that includes the `uploadId`. (Body shape shown below.) [\[postman.com\]](https://www.postman.com/insead-apis/workspace/higher-ed-rest-apis/request/270142-4b9cd952-d213-4b8a-915a-59589ea90698)

> Background: the “uploads” endpoint is the standard way to stage any file for later use by other REST endpoints; the assignments docs show this pattern explicitly. [\[docs.anthology.com\]](https://docs.anthology.com/docs/blackboard/rest-apis/advanced/ultra-assignments), [\[blackboard.github.io\]](https://blackboard.github.io/rest-apis/learn/advanced/ultra-assignments)

***

## Entitlements and prerequisites

*   **Register the REST app** in Anthology’s Developer Portal and **enable** it in Learn (Admin → Integrations → REST API Integrations). [\[help.blackboard.com\]](https://help.blackboard.com/Learn/Administrator/SaaS/Integrations/Compare_Building_Blocks_and_Rest), [\[support.an...hology.com\]](https://support.anthology.com/s/article/The-Blackboard-REST-API-Framework?language=en_US)
*   **Auth:** Obtain an OAuth 2.0 **Bearer token** (two‑legged or three‑legged). Tokens typically expire in \~1 hour. [\[blackboard.github.io\]](https://blackboard.github.io/rest-apis/learn/examples/curl-demo)
*   **Permissions:**
    *   To update your **own** avatar, callers need `self.user.MODIFY`.
    *   To update **other users**, you’ll need `system.user.properties.MODIFY` (and sometimes more granular entitlements depending on fields). [\[postman.com\]](https://www.postman.com/insead-apis/workspace/higher-ed-rest-apis/request/270142-4b9cd952-d213-4b8a-915a-59589ea90698)

***

## Step‑by‑step with cURL

> Replace `https://your-learn-host` and IDs with values for your environment.

### 1) Get an access token

```bash
curl -s -X POST \
  -H "Authorization: Basic <base64(clientKey:clientSecret)>" \
  -d "grant_type=client_credentials" \
  https://your-learn-host/learn/api/public/v1/oauth2/token
```

Keep `access_token` from the JSON response. [\[blackboard.github.io\]](https://blackboard.github.io/rest-apis/learn/examples/curl-demo)

### 2) Upload the avatar image

```bash
curl -s -X POST \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/octet-stream" \
  --data-binary @./avatar-150x150.jpg \
  "https://your-learn-host/learn/api/public/v1/uploads?fileName=avatar-150x150.jpg"
```

**Response:** JSON that includes `"id": "<UPLOAD_ID>"`. That **uploadId** is your handle to the file in Learn. [\[docs.anthology.com\]](https://docs.anthology.com/docs/blackboard/rest-apis/advanced/ultra-assignments), [\[blackboard.github.io\]](https://blackboard.github.io/rest-apis/learn/advanced/ultra-assignments)

> Tip: Use a square \~**150×150 px** image; larger images are clipped in Learn’s avatar UI. (Admin help guidance.) [\[help.blackboard.com\]](https://help.blackboard.com/Learn/Administrator/Hosting/User_Management/Avatars)

### 3) Patch the user to set the avatar

```bash
curl -s -X PATCH \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
        "avatar": {
          "source": "User",
          "uploadId": "<UPLOAD_ID>"
        }
      }' \
  "https://your-learn-host/learn/api/public/v1/users/<USER_ID>"
```

This associates the uploaded file with the user’s avatar. The body shape (including `avatar.source` and `avatar.uploadId`) is shown in public examples of the **Update User** request. [\[postman.com\]](https://www.postman.com/insead-apis/workspace/higher-ed-rest-apis/request/270142-4b9cd952-d213-4b8a-915a-59589ea90698)

***

## Removing or changing a user avatar

*   **Replace**: Repeat the upload and PATCH steps with a new file (same payload; just a new `uploadId`). [\[docs.anthology.com\]](https://docs.anthology.com/docs/blackboard/rest-apis/advanced/ultra-assignments), [\[blackboard.github.io\]](https://blackboard.github.io/rest-apis/learn/advanced/ultra-assignments)
*   **Remove** (revert to silhouette): In practice, you can PATCH the user and clear the avatar or set policy to show the generic silhouette via Admin avatar settings. (Admin‑side controls: **Allow users to upload** vs **Admin‑assigned avatars**, batch upload, delete inappropriate avatars.) [\[help.blackboard.com\]](https://help.blackboard.com/Learn/Administrator/Hosting/User_Management/Avatars)

***

## Verifying

*   **Read back** the user via `GET /learn/api/public/v1/users/{userId}` (specify `fields=avatar` if you want to minimize payload) and/or fetch the avatar image (the fetch returns a **redirect** to the image URL; follow it to view). [\[bblearn.re...thedocs.io\]](https://bblearn.readthedocs.io/en/latest/pages/api.html)

***

## Common pitfalls & best practices

*   **Image size & aspect ratio:** Stick to **150×150** square to avoid clipping. [\[help.blackboard.com\]](https://help.blackboard.com/Learn/Administrator/Hosting/User_Management/Avatars)
*   **Token handling:** Token reuse is fine until expiry; there’s no refresh token in the basic flow—request a new token when needed. [\[blackboard.github.io\]](https://blackboard.github.io/rest-apis/learn/examples/curl-demo)
*   **Entitlements:** If your PATCH returns 403, check that the integration user has the required `system.user.properties.MODIFY` (or that you’re using 3‑legged OAuth as the actual user for `self.user.MODIFY`). [\[postman.com\]](https://www.postman.com/insead-apis/workspace/higher-ed-rest-apis/request/270142-4b9cd952-d213-4b8a-915a-59589ea90698)
*   **Governance:** Many institutions prefer end‑user uploads via the **Profile** page; admins can control whether uploads are allowed in **Admin → Avatars**. [\[help.blackboard.com\]](https://help.blackboard.com/Learn/Administrator/SaaS/Ultra_Experience/Base_Navigation/Profile)

***

## Why this works (documentation trail)

*   The **uploads** endpoint is documented as the way to stage files for subsequent REST operations: “Make a POST request to `/learn/api/public/v1/uploads`. **Use the ID number in the response** to further access the uploaded file.” [\[docs.anthology.com\]](https://docs.anthology.com/docs/blackboard/rest-apis/advanced/ultra-assignments), [\[blackboard.github.io\]](https://blackboard.github.io/rest-apis/learn/advanced/ultra-assignments)
*   Community/API references for **Update User** show an `avatar` object that takes an `uploadId`, enabling you to wire the staged file to the user’s avatar. [\[postman.com\]](https://www.postman.com/insead-apis/workspace/higher-ed-rest-apis/request/270142-4b9cd952-d213-4b8a-915a-59589ea90698)
*   Admin help continues to document avatar behavior, sizing, and the batch/approval workflow for institutions. [\[help.blackboard.com\]](https://help.blackboard.com/Learn/Administrator/Hosting/User_Management/Avatars)

***

If you’d like, I can put together a small script (Python or PowerShell) that:

*   Reads a CSV of `userId, path_to_image`,
*   Uploads each image,
*   PATCHes each user’s avatar with the returned `uploadId`,
*   Logs successes/failures with entitlement hints.

What’s your deployment (SaaS or Managed/Self‑Hosted) and preferred language?
