import os
import hashlib
import re
from datetime import datetime


pypi_handler_templates_dir = "pypi_handler_templates"
github_action_path = os.environ.get('GITHUB_ACTION_PATH')
github_workspace = os.environ.get('GITHUB_WORKSPACE')
root_index_template_filename = "root-index.html"
root_item_template_filename = "root-item.html"
package_index_template_filename = "package-index.html"
package_item_template_filename = "package-item.html"
root_item_replace_string = "</body>"
package_item_replace_string = "</ul>"
print(f"GITHUB_ACTION_PATH: {github_action_path}")
print(f"GITHUB_WORKSPACE: {github_workspace}")

def ensure_dir_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def normalize(name):
    """Normalize package names according to the specification."""
    return re.sub(r"[-_.]+", "-", name).lower()

# must have: <ul></ul>
default_root_index_template_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Private PyPI Index</title>
</head>
<body>
</body>
</html>"""

default_root_item_template_html="""<li>
  <a href="{full_url}">{package_name}</a>
</li>"""

default_package_index_template_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{package_name}</title>
</head>
<body>
    <h1>{package_name}</h1>
    <ul></ul>
</body>
</html>"""

default_package_item_template_html="""<li>
    <a href="{archive_url}#egg={package_name}-{version}">
        {package_name}-{version}
    </a>
    ({version}, {timestamp})
</li>"""


# generic function to get a template
def get_template(template_filename, default_template):
    try:
        template_path_a = f"{github_action_path}/{pypi_handler_templates_dir}/{template_filename}"
        template_path_w = f"{github_workspace}/{pypi_handler_templates_dir}/{template_filename}"

        html_template = None
        print(f"Gathering templates.")
        # if there is a file in the workspace, use that as the index
        print(f"  looking for template in workspace: {template_path_w}")
        if os.path.exists(template_path_w):
            print(f"    found!")
            with open(template_path_w, 'r') as file:
                html_template = file.read()

        print(f"  looking for template in action: {template_path_a}")
        if os.path.exists(template_path_a) and not html_template:
            print(f"    found!")
            with open(template_path_a, 'r') as file:
                html_template = file.read()

        # if no template is found, use the default
        if not html_template:
            print(f"  no template found, using default.")
            html_template = default_template
        
        return html_template
    except Exception as e:
        print(f"An error occurred while getting the template: {e}")

# function to get root index template
def get_root_index_template():
    return get_template(root_index_template_filename, default_root_index_template_html)

# function to get root item template
def get_root_item_template():
    return get_template(root_item_template_filename, default_root_item_template_html)

# function to get package index template
def get_package_index_template():
    return get_template(package_index_template_filename, default_package_index_template_html)

# function to get package item template
def get_package_item_template():
    return get_template(package_item_template_filename, default_package_item_template_html)

# function to return html for the root index
# given the following variables
# package_name: the name of the package
# base_url: the base url to use for the package
# returns the html
def get_root_index_html(package_name, base_url, existing_html=""):
    # Check if the package name already exists in the index
    # if base_url is not provided
    if not base_url:
        full_url = f"{package_name}/"
    else:
        full_url = f"{base_url}/{package_name}/"


    # if existing_html is not provided, use the template
    if not existing_html:
        # get the index template
        print("Getting template for root index.")
        index_html_template = get_root_index_template()
        index_html = index_html_template
    else:
        print("Using existing index.")
        index_html = existing_html

    print("Getting template for root item.")
    root_item_template = get_root_item_template()

    print("  Rendering item html")
    root_item_html=root_item_template.format(package_name=package_name, base_url=base_url, full_url=full_url)
    
    print(f"Checking if package name is in index.")
    if f'href="{full_url}"' not in index_html:
        # Insert the new package link before the closing body tag
        index_html = index_html.replace(root_item_replace_string, f"\n{root_item_html}\n{root_item_replace_string}")

    return index_html

def update_root_index(index_path, package_name, base_url):
    try:
        # Read the existing index data
        print(f"Reading existing index at {index_path}.")
        existing_html = ""
        if os.path.exists(index_path):
            print(f"Index exists at {index_path}.")

            print(f"Opening index at {index_path}.")
            with open(index_path, 'r') as file:
                print(f"Reading index at {index_path}.")
                existing_html = file.read()
        else:
            print(f"Index does not exist at {index_path}.")

        index_html = get_root_index_html(package_name, base_url, existing_html)

        # Write the updated index data back to the file
        with open(index_path, 'w') as file:
            file.write(index_html)
        
        print(f"Upserted {package_name} into index successfully.")
    except Exception as e:
        print(f"An error occurred while upserting the index: {e}")

# function to return html for the package index
# given the following variables
# package_name: the name of the package
# version: the version of the package
# archive_url: the url to the archive
# archive_sha256: the sha256 hash of the archive
# returns the html
def get_package_index_html(package_name, version, archive_url, archive_sha256, existing_html=""):
    # if archive_sha256 is not provided, attach to link
    if not archive_sha256:
        link = f"<a href='{archive_url}'>"
    else:
        link = f"<a href='{archive_url}#sha256={archive_sha256}'>"

    link=f"{link}\n  {package_name}-{version}\n</a>"

    # if existing_html is not provided, use the template
    if not existing_html:
        # get the index template
        print("Getting template for package index.")
        index_html_template = get_package_index_template()
        index_html = index_html_template.format(package_name=package_name)
    else:
        print("Using existing index.")
        index_html = existing_html

    print("Getting template for package item.")
    package_item_template = get_package_item_template()

    print("  Rendering item html")
    package_item_html=package_item_template.format(package_name=package_name, version=version, archive_url=archive_url, archive_sha256=archive_sha256, timestamp=datetime.now().isoformat())
    
    print(f"Checking if link is in index.")
    if link not in index_html:
        # Insert the new link and version info before the closing ul tag
        index_html = index_html.replace(package_item_replace_string, f"{package_item_html}\n{package_item_replace_string}")

    return index_html


# function to update the package index
def update_package_index(package_dir, package_name, version, archive_url, archive_sha256):
    try:
        print("update_package_index:")
        print(f"package_dir: {package_dir}")
        print(f"package_name: {package_name}")
        print(f"version: {version}")
        print(f"archive_url: {archive_url}")
        print(f"archive_sha256: {archive_sha256}")

        # ensure the package directory exists
        print(f"Ensuring package directory {package_dir} exists.")
        ensure_dir_exists(package_dir)

        # get the package index path
        package_index_path = os.path.join(package_dir, "index.html")

        # Read the existing index data
        print(f"Reading existing index at {package_index_path}.")
        if os.path.exists(package_index_path):
            print(f"Index exists at {package_index_path}.")

            print(f"Opening index at {package_index_path}.")
            with open(package_index_path, 'r') as file:
                print(f"Reading index at {package_index_path}.")
                index_html = file.read()
        else:
            print(f"Index does not exist at {package_index_path}.")

        index_html = get_package_index_html(package_name, version, archive_url, archive_sha256, index_html)

        # Write the updated index data back to the file
        with open(package_index_path, 'w') as file:
            file.write(index_html)
        
        print(f"Upserted {package_name} version {version} into index successfully.")
    except Exception as e:
        print(f"An error occurred while upserting the index: {e}")

def upsert_package(root_dir, package_name, version, archive_url, archive_sha256, base_url):
    package_name_normalized = normalize(package_name)
    print(f"Upserting package {package_name_normalized} version {version} from {archive_url}.")

    # ensure the root directory exists
    print(f"Ensuring root directory {root_dir} exists.")
    ensure_dir_exists(root_dir)

    # update the root index
    print(f"Updating root index at {os.path.join(root_dir, 'index.html')}.")
    update_root_index(os.path.join(root_dir, "index.html"), package_name_normalized, base_url)


    package_dir = os.path.join(root_dir, package_name_normalized)
    update_package_index(package_dir, package_name_normalized, version, archive_url, archive_sha256)

# set up main
if __name__ == "__main__":

    # env vars:
    # root_dir
    # python_service_name
    # python_service_version
    # python_service_archive_url
    root_dir = os.environ.get('root_dir')
    package_name = os.environ.get('python_service_name')
    version = os.environ.get('python_service_version')
    archive_url = os.environ.get('python_service_archive_url')
    archive_sha256 = os.environ.get('python_service_archive_sha256')

    print(f"root_dir: {root_dir}")
    print(f"package_name: {package_name}")
    print(f"version: {version}")
    print(f"archive_url: {archive_url}")
    print(f"archive_sha256: {archive_sha256}")
    base_url = os.environ.get('base_url')
    print("calling upsert_package")
    upsert_package(root_dir, package_name, version, archive_url, archive_sha256, base_url)