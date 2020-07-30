# Database schema
### Terminology
- `A^B` => Column `A` references table `B`
- `A_o` => Column is optional
- **A** => key

### Schema
- Server(**serverID**, name_o, inviteLink_o)
- Category(**serverID^Server, catName**)
- Post(**serverID^Category, catName^Category, title**, subtitle, content, credits)
- Role(**serverID^Server, roleID**)

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
- Category
  - serverID = NUMERIC
  - roleID = NUMERIC