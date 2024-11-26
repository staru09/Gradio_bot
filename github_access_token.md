
# How to Fetch a GitHub Access Token

Follow these steps to generate a Personal Access Token (PAT) from GitHub:

---

## **Step 1: Log in to GitHub**
1. Log in with your GitHub credentials.

---

## **Step 2: Navigate to Developer Settings**
1. Click on your profile picture in the top-right corner of the page.
2. Select **Settings** from the dropdown menu.
3. Scroll down to the **Developer settings** section on the left-hand sidebar and click it.

---

## **Step 3: Create a New Personal Access Token**
1. Click on **Personal access tokens** and then **Tokens (classic)**.
2. Click the **Generate new token** button.

---

## **Step 4: Configure the Token**
1. **Add a Note**: Enter a descriptive note for the token, such as "GitHub API Access".
2. **Set Expiration**: Choose an expiration period (e.g., 30 days, 60 days) or select **No expiration** for unlimited validity.
3. **Select Scopes**:
   - Choose the appropriate permissions for your token. For example:
     - `repo` for accessing private and public repositories.
     - `read:org` for reading organization data.
     - `workflow` for managing workflows.
4. Click **Generate token** at the bottom of the page.

---

## **Step 5: Copy and Store the Token**
1. Once the token is generated, **copy it immediately**. You won't be able to view it again.
2. Store the token securely in a password manager or a secure environment variable.

---

## **Step 6: Use the Token**
You can use the token in place of your password for Git operations or in API calls. For example:

### **Using in API:**
Include the token in the `Authorization` header:
```bash
curl -H "Authorization: token <your_access_token>" https://api.github.com/user
```

---

**Warning:** Never expose your personal access token in public repositories or shared environments.

---
