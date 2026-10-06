from veracode_api_py import Applications, Sandboxes
import sys

def get_app_guid(app_name):
    application_candidates = Applications().get_by_name(app_name)
    if not application_candidates:
        return None
    for app in application_candidates:
        if app["profile"]["name"] == app_name:
            return app["guid"]
    return None

def get_oldest_sandbox(sandbox_list):
    if not sandbox_list:
        return None
    oldest_sandbox = min(sandbox_list, key=lambda x: x["modified"])
    return oldest_sandbox

def main():
    args = sys.argv[1:]
    
    if not args:
        print("Please provide the path to the applications list file.")
        return

    app_guid = get_app_guid(args[0])
    if app_guid is None:
        print(f"No application found with the name '{args[0]}'.")
        return

    sandbox_list = Sandboxes().get_all(app_guid)
    if not sandbox_list:
        print(f"No sandboxes found for application '{args[0]}'.")
        return

    if len(sandbox_list) < 10:
        print("The application has fewer than 10 sandboxes. Skipping cleanup.")
        return

    sandbox_to_delete = get_oldest_sandbox(sandbox_list)
    if sandbox_to_delete:
        print(f"Deleting sandbox '{sandbox_to_delete['name']}' (GUID: {sandbox_to_delete['guid']})...")
        Sandboxes().delete(app_guid, sandbox_to_delete["guid"])
        print("Sandbox deleted successfully.")
    else:
        print("No sandbox found to delete.")


if __name__ == "__main__":
    main()
