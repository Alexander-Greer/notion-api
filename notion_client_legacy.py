import requests
import json


from notion_blocks import NotionBlock, BookmarkBlock, BreadcrumbBlock, BulletItemBlock, \
    CalloutBlock, CodeBlock, ColumnsBlock, DividerBlock, EmbedBlock, EquationBlock, FileBlock, H1Block, \
    H2Block, H3Block, ImageBlock, MentionBlock, NumberedItemBlock, ParagraphBlock, PDFBlock, \
    QuoteBlock, SyncedBlockSource, SyncedBlockDuplicate, TableBlock, TableOfContentsBlock, \
    ToDoBlock, ToggleBlock, VideoBlock



NOTION_COLORS = {
    'gray', 'lightgray', 'brown', 'yellow', 'orange',
    'green', 'blue', 'purple', 'pink', 'red'
}


class NotionClient:
    """
    Creates a framework through which the user can interact with a Notion workspace
    Stores information about the API token ("integration secret")
        and about the required request headers (based on the token)
    """
    def __init__(self, token):
        """
        :param token: Internal integration "secret" from Integrations page
            https://www.notion.so/my-integrations
        """
        self.token = token
        self.headers = self.make_headers(token)
        self.databases = {}
        self.pages = {}

    @staticmethod
    def make_headers(token):
        # https://www.python-engineer.com/posts/notion-api-python/
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",  # https://developers.notion.com/reference/versioning
        }
        return headers

    def connect_database(self, database_id):
        # self.databases[database_id] = NotionDB(self, database_id)
        # return database_id
        db_obj = NotionDB(self, database_id)
        self.databases[database_id] = db_obj
        return db_obj

    def get_database(self, database_id):
        return self.databases.get(database_id)

    def connect_page(self, page_obj):
        """
        :param page_obj: object of type NotionPage
        :return:
        """
        page_id = page_obj.get_page_id()
        self.pages[page_obj.get_page_id()] = page_obj
        return self.pages[page_id]


class NotionDB:
    def __init__(self, client, database_id):
        self.client = client
        self.database_id = database_id

    # https://www.python-engineer.com/posts/notion-api-python/
    def add_entry(self, entry_properties, debug=False):
        """
        Adds a new 'page' (entry) to the database specified by DATABASE_ID
        :param entry_properties: a dictionary storing the parameters to be input for the database entry, e.g.
            db_data = {
                "Title": {"title": [{"text": {"content": "This is the recipe title."}}]},
                "Recipe Link": {"url": "www.google.com"}
            }
        :param debug: print the post request response?
        :return: the response from the POST request to the database
        """
        post_url = "https://api.notion.com/v1/pages"
        payload = {"parent": {"database_id": self.database_id}, "properties": entry_properties}

        res = requests.post(post_url, headers=self.client.headers, json=payload)
        if res.status_code == 200:
            print(f"{res.status_code}: Entry added successfully")
        else:
            print(f"{res.status_code}: Error during entry addition")

        if debug:
            print(res)

        return res

    # https://medium.com/@plasmak_/how-to-create-a-notion-page-using-python-9994bf01299
    def edit_entry_page(self, entry_page_id, page_content: dict, debug=False):
        """
        Performs a PATCH request to update the content of the database entry Title page
        :param entry_page_id: hex string representing the page id, e.g.
            page_block_id = "faeb6c55-e216-46d1-abed-2b706443d48a"
        :param page_content: a JSON-like dictionary containing the content to be added to the page
        :param debug: print the patch request response?
        :return: the response from the PATCH request to the database
        """
        edit_url = f"https://api.notion.com/v1/blocks/{entry_page_id}/children"

        res = requests.patch(edit_url, headers=self.client.headers, json=page_content)
        if res.status_code == 200:
            print(f"{res.status_code}: Entry edited successfully")
        else:
            print(f"{res.status_code}: Error during entry editing")

        if debug:
            print(res)

        return res

    def edit_page_properties(self, entry_page_id, properties_json: dict, debug=False):
        """
        https://developers.notion.com/reference/patch-page
        :param entry_page_id:
        :param properties_json:
        :param debug:
        :return:
        """

        # edit page cover https://baldbeardedbuilder.com/blog/how-to-update-notion-cover-image-with-javascript/

        edit_url = f'https://api.notion.com/v1/pages/{entry_page_id}'

        res = requests.patch(edit_url, headers=self.client.headers, json=properties_json)
        if res.status_code == 200:
            print(f"{res.status_code}: Entry edited successfully")
        else:
            print(f"{res.status_code}: Error during entry editing")

        if debug:
            print(res, res.content)

        return res

    def edit_page_cover(self, entry_page_id, cover_image_url, debug=False):
        # edit page cover https://baldbeardedbuilder.com/blog/how-to-update-notion-cover-image-with-javascript/
        properties_json = {
            "cover": {
                "type": "external",
                "external": {
                    "url": cover_image_url
                }
            }
        }

        edit_url = f'https://api.notion.com/v1/pages/{entry_page_id}'

        res = requests.patch(edit_url, headers=self.client.headers, json=properties_json)
        if res.status_code == 200:
            print(f"{res.status_code}: Entry edited successfully")
        else:
            print(f"{res.status_code}: Error during entry editing")

        if debug:
            print(res, res.content)

        return res

    def edit_page_icon(self, entry_page_id, emoji=None, notion_icon_name=None, notion_icon_color='lightgray', debug=False):
        if emoji is not None:
            properties_json = {
                "icon": {
                    "type": "emoji",
                    "external": emoji
                }
            }
        if notion_icon_name is not None:
            if notion_icon_color not in NOTION_COLORS:
                notion_icon_color = 'lightgray'
            icon_url = f'https://www.notion.so/icons/{notion_icon_name}_{notion_icon_color}.svg'
            properties_json = {
                'icon': {
                    'type': 'external',
                    'external': {
                        # e.g. https://www.notion.so/icons/pitcher_gray.svg
                        'url': icon_url
                    }
                }
            }

        edit_url = f'https://api.notion.com/v1/pages/{entry_page_id}'

        res = requests.patch(edit_url, headers=self.client.headers, json=properties_json)
        if res.status_code == 200:
            print(f"{res.status_code}: Entry edited successfully")
        else:
            print(f"{res.status_code}: Error during entry editing")

        if debug:
            print(res, res.content)

        return res

    # https://www.python-engineer.com/posts/notion-api-python/
    def get_pages(self, num_pages=None, debug=False):
        """
        If num_pages is None, get all pages, otherwise just the defined number.
        """
        url = f"https://api.notion.com/v1/databases/{self.database_id}/query"

        get_all = num_pages is None
        page_size = 100 if get_all else num_pages

        payload = {"page_size": page_size}
        response = requests.post(url, json=payload, headers=self.client.headers)

        data = response.json()
        if debug:
            print(json.dumps(data, indent=2))

        # Comment this out to dump all data to a file
        # import json
        # with open('page_data.json', 'w', encoding='utf8') as f:
        #    json.dump(data, f, ensure_ascii=False, indent=4)

        results = data["results"]
        while data["has_more"] and get_all:
            payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
            url = f"https://api.notion.com/v1/databases/{self.database_id}/query"
            response = requests.post(url, json=payload, headers=self.client.headers)
            data = response.json()
            results.extend(data["results"])

        return results

    def get_database_obj(self, debug=False):
        """
        Retrieves the database object as columns rather than rows/pages
        https://developers.notion.com/reference/retrieve-a-database
        :param debug:
        :return:
        """

        url = f"https://api.notion.com/v1/databases/{self.database_id}"

        response = requests.get(url, headers=self.client.headers)

        data = response.json()
        if debug:
            print(json.dumps(data, indent=2))

        return data

    # https://www.pynotion.com/getting-started-with-python
    def get_page_content(self, page_id):
        res = requests.get(f"https://api.notion.com/v1/blocks/{page_id}/children", headers=self.client.headers)
        if res.status_code == 200:
            print(f"{res.status_code}: Retrieved successfully")
        else:
            print(f"{res.status_code}: Error during page retrieval")
        return res.json()


class NotionPage:
    def __init__(self, client, page_url=None, page_id=None):
        """
        :param client: NotionClient object
        :param page_id: 32-character hexadecimal string; found at the end of the URL saved
            when "Copy Link" is clicked on the page

            e.g. https://www.notion.so/2-Jan-2024-8047540ed15046a3a7c24f8c7890ffb1?pvs=4
                -> "8047540ed15046a3a7c24f8c7890ffb1"
        """
        self.client = client

        if page_url is not None:
            split_url = page_url.split("notion.so/")
            self.page_id = split_url[1].replace("?pvs=4", "")[-32:]
        else:
            self.page_id = page_id

    def get_page_id(self):
        return self.page_id

    # https://www.pynotion.com/getting-started-with-python
    def get_page_content(self):
        """
        Pulls the content of a Notion page as a JSON object
        Ensure the page specified is connected to the Integration related to the
            client's API token
        :return: the JSON object returned from the GET request to the Notion page containing the page content
        """
        res = requests.get(f"https://api.notion.com/v1/blocks/{self.page_id}/children", headers=self.client.headers)
        if res.status_code == 200:
            print(f"{res.status_code}: Retrieved successfully")
        else:
            print(f"{res.status_code}: Error during page retrieval")
        return res.json()

    def add_block(self, block: NotionBlock, return_id=False, debug=False):
        """
        Performs a PATCH request to update th content of the database entry Title page
        :param block: a NotionBlock object to be added to the page
        :param return_id: return the entire PATCH response or just the page ID
        :param debug: whether to print the patch request
        :return: the response from the PATCH request to the Notion page
        """
        edit_url = f"https://api.notion.com/v1/blocks/{self.page_id}/children"

        res = requests.patch(edit_url, headers=self.client.headers, json=block.json_content)
        if res.status_code == 200:
            print(f"{res.status_code}: Entry edited successfully")
        else:
            print(f"{res.status_code}: Error during entry editing")

        if debug:
            print(res, res.content)

        # https://stackoverflow.com/questions/49184578/how-to-convert-bytes-type-to-dictionary
        # the response content is a bytestring; convert to a JSON obj / dict
        response_obj = json.loads(res.content.decode('utf-8'))

        if response_obj.get("status") == 400:
            if "path failed validation" in response_obj.get("message"):
                raise ValueError("Response returned 400 - check to make sure"
                                 " the target page has been connected to the API integration.")

        if not return_id:
            return response_obj
        else:
            return response_obj.get('results')[0].get('id')
