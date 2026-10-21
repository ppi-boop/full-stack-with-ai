# 02 — Client-Server, HTTPS, Terminal & Permissions Cheat Sheet

> **Quick Summary:** Stateless HTTP, TLS security triad, path resolution, and Unix permission models.

---

## 1. Client-Server & Statelessness

* **Statelessness:** Server retains zero memory between requests. Each request must be self-sufficient.
* **Maintaining Sessions:**
  * **HttpOnly Cookies:** Automatically attached by browser; inaccessible to JavaScript (XSS safe).
  * **Authorization Header:** `Bearer <JWT_TOKEN>` verified cryptographically by the server per request.
* **The React State Anti-Pattern:** Never rely on `useState(isLoggedIn)` as a security boundary. A browser refresh wipes it, and client-side memory can be tampered with in DevTools. The backend must verify the token on every request.

---

## 2. The HTTPS (TLS) Triad

HTTPS is standard HTTP inside an encrypted TLS tunnel. It guarantees three essentials:

| Pillar | Protection | Real-World Scenario |
|---|---|---|
| **1. Encryption** | Confidentiality | Prevents eavesdropping on public Wi-Fi (Wireshark packet sniffing). |
| **2. Integrity** | Anti-Tampering | Detects if an attacker alters payload data in transit. |
| **3. Authentication** | Identity Proof | Certificate Authorities (CAs) verify you are connected to the genuine domain. |

> **Localhost Exception:** Browsers allow `http://localhost` without warnings because traffic stays on the internal loopback interface (`127.0.0.1`).

---

## 3. Terminal & Shell Essentials

* **Terminal:** The display application (iTerm2, Terminal.app, VS Code terminal).
* **Shell:** The command language interpreter (`zsh` on macOS, `bash` on Linux, `PowerShell` on Windows).

### Essential Command Matrix

| Task | macOS / Linux | Windows PowerShell |
|---|---|---|
| Print working directory | `pwd` | `pwd` |
| List all files (including hidden) | `ls -la` | `ls -Force` |
| Move up one folder | `cd ..` | `cd ..` |
| Create nested directories | `mkdir -p a/b/c` | `mkdir a\b\c` |
| Create empty file | `touch file.txt` | `ni file.txt` |
| Recursive copy / move | `cp -r src/ dest/`, `mv old new` | `cp -r`, `mv` |
| Search text in files | `grep -rn "keyword" .` | `Select-String -Path * -Pattern "keyword"` |
| Locate executable path | `which node` | `where.exe node` |

---

## 4. Paths: Absolute vs Relative

* **Absolute:** Starts from root (`/Users/tagline/...` on Unix, `C:\Users\...` on Windows). Location-independent.
* **Relative:** Starts from current location (`pwd`):
  * `./` = current folder
  * `../` = parent folder
* **Cross-Platform Safety:** Windows uses `\`, Unix uses `/`. Always use `path.join()` in Node.js:
  ```javascript
  import path from "node:path";
  const filePath = path.join(__dirname, "data", "users.json");
  ```

---

## 5. Unix Permissions & `chmod`

Format from `ls -l`: `-rwxr-xr--` (10 characters: type + Owner + Group + Others).

### The Math (Octal Values)
* **`r` (Read) = 4**
* **`w` (Write) = 2**
* **`x` (Execute) = 1**
* **`-` (None) = 0**

### Common Permission Combinations
* **`chmod 755 file`**:
  * Owner: `4+2+1 = 7` (Read, Write, Execute)
  * Group: `4+0+1 = 5` (Read, Execute)
  * Others: `4+0+1 = 5` (Read, Execute)
  * *Standard for scripts and executable programs.*
* **`chmod 644 file`**:
  * Owner: `4+2+0 = 6` (Read, Write)
  * Group: `4+0+0 = 4` (Read only)
  * Others: `4+0+0 = 4` (Read only)
  * *Standard for source code and config files.*
* **`chmod 777 file`** $\rightarrow$ **Anti-pattern**: Anyone can overwrite or execute the file.

---

## 6. Critical Production Traps

1. **Empty Variable in `rm -rf`:**
   ```bash
   rm -rf $TARGET_DIR/ # If $TARGET_DIR is empty, this runs rm -rf / !
   ```
   *Mitigation:* Check variables and run `pwd` before recursive deletions.
2. **`sudo npm install` is toxic:**
   * Grants root privileges to third-party `postinstall` scripts.
   * Creates root-owned files that generate persistent `EACCES` permission errors for normal users.
