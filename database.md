# Database schema
### Terminology
- `A^B` => Column `A` references table `B`
- `A_o` => Column is optional
- <span style="text-decoration: underline">A</span> => key

### Schema
- Server(<span style="text-decoration: underline">serverID</span>, name_o, inviteLink)
- Category(<span style="text-decoration: underline">serverID^Server, catName</span>)
- Post(<span style="text-decoration: underline">serverID^Category, catName^Category, title</span>, subtitle, content, credits)

### Attribute Domains
- Server
  - serverID = NUMERIC
  - name = VARCHAR(32)
  - inviteLink = VARCHAR(128)
- Category
  - serverID = NUMERIC
  - catName = VARCHAR(32)
- Post
  - serverID = NUMERIC
  - catName = VARCHAR(32)
  - title = VARCHAR(64)
  - subtitle = VARCHAR(128)
  - content = TEXT