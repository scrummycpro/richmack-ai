- `id`: Unique identifier for each record
- `link`: The link entered by the user
- `position`: Position details entered by the user
- `notes`: Additional notes related to the link (optional)
- `source`: Source of the link (LinkedIn, Indeed, or Other)
- `upload_resume`: Boolean indicating whether a custom resume should be uploaded
- `timestamp`: Current timestamp when the link is saved to the database

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


sqlite3 links.db "SELECT notes FROM links;" > allnotes.txt

grep -ow '[A-Z][a-zA-Z]\{3,\}' allnotes.txt > allnotes-words.txt
