Defines a `NotionClient` class which can be used to interact with a Notion integration.

Currently supports the creation of the following block types:

  *Bookmark, Breadcrumb, Bulleted List Item, Callout, Code, Divider, Embed, 
  Equation, File, H1, H2, H3, Image, Mention, Numbered List Item, Paragraph,
  PDF, Quote, Synced Block Source, Synced Block Duplicate, Table Of Contents, 
  To Do, Toggle, Video*

To use, first create an internal integration using the integration dashboard at https://www.notion.so/my-integrations

  This will create an integration linked to your Notion account that you can access from any page (see below) whenever you are logged in.

Then get the "Internal Integration Secret" for your integration from the same page.

(It should look something like "secret_XXX..." where XXX.. is a long string of letters and numbers.)

Declare a variable in your Python project to store this token for use, something like:

`token = "secret_XXX..."`

For whichever base Notion page you wish to interact with, ensure it is connected to the integration.
  - In the Notion app, on the page you want, click the three dots in the upper right.
  - Scroll down to "Connections" and click "+ Add connections".
  - Search for the *name* of your integration in the list menu and click to add.

In your Python project, define a client object via the following:

`client = NotionClient(token)`

To link and edit a database, get the database ID and store it as a variable like

`database_id = "XXX..."` (where XXX... is a 32-character hexadecimal hash from the database URL)

  (If your URL looks like "https://www.notion.so/<long_hash_1>?v=<long_hash_2>",
  then <long_hash_1> is the database ID and <long_hash_2> is the view ID.)

`client.connect_database(database_id)`

`database_obj = client.get_database(database_id)`

You can add entries to the database as follows, provided you know the format of the existing columns:

(The entry data in the below example consists of a `Text` type column and a `URL` type column.)

`new_entry_data = {
    <Database_column_name_1>: {"title": [{"text": {"content": recipe_title}}]},
    <Database_column_name_2>: {"url": recipe_link}
}`

`database_obj.add_entry(new_entry_data)`
