from datetime import datetime, timedelta
import requestservice
import calendarservice

CULL_AFTER_DAYS_NUMBER = 7

def should_cull(request_data):
    approval = request_data["approval"]
    request_date = datetime.strptime(request_data["date"], "%Y-%m-%d")

    age = datetime.now()-request_date

    is_too_old = age >= timedelta(days=CULL_AFTER_DAYS_NUMBER)
    
    ## Requests that are pending or denied and too old should be culled
    cull = (approval == "Pending" and is_too_old) or (approval == "Denied" and is_too_old)
    
    return cull

def cleanup_requests():
    requests = requestservice.get_all_requests()
    deleted_count = 0

    for request_id, request_data in requests.items():
        if should_cull(request_data):

            event_id = request_data.get("event_id")
            print(f"Culling request {request_id}...")

            ## Here i'm trying to delete a google calendar event, which i'm slightly dubious about
            ## we'll try to handle it gracefully with an exception
            if event_id:
                try:
                    calendarservice.delete_event(event_id)
                    print(f"!! Deleted calendar event {event_id} !!")
                except Exception as e:
                    print(f"Failed to delete calendar event {event_id}: {e}")
            
            ## Here i'm deleting from the db, again might as well use an exception
            try:
                requestservice.delete_request(request_id)
                print(f"!! Deleted request: {request_id} !!")
                deleted_count += 1
            except Exception as e:
                print(f"Failed to delete request {request_id}: {e}")

    print(f"Cleanup complete! Deleted {deleted_count} requests!")

if __name__ == "__main__":
    cleanup_requests()
