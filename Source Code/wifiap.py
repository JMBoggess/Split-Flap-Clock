import asyncio
import network
from response import Response

class WIFIAP:
    """
    Configures wifi as an Access Point
    """

    def __init__(self, event_config_exit):
        """
        Setup the AP network

        event_config_exit (asyncio.Event) - Event for indicating to the program the configuration mode is exiting
        """
        self.ssid = 'WifiSetup'
        self.ap = network.WLAN(network.AP_IF)
        self.ap.config(ssid=self.ssid)
        self.event_config_exit = event_config_exit
    
    async def start_server(self, print_status=False):
        """
        Start the AP server and listen for requests

        print_status (bool) - print message to console (used during development and debugging)
        """
        self.ap.active(True)
        self.server = await asyncio.start_server(self.serve_request, '0.0.0.0', 80)
        
        if print_status:
            print('Server started')
            print(f'Connect to network (ssid): {self.ssid} with password: picoW123')
            print('Then browse to 192.168.4.1 to setup wifi')
    
    def stop_server(self):
        if self.server:
            self.server.close()
        self.ap.active(False)

    async def serve_request(self, sreader: asyncio.StreamReader, swriter: asyncio.StreamWriter):
        """
        Serves requests sent to this Access Point
        """
        # Read the request
        request_line = await sreader.readline()

        # Debug print
        # print(request_line.decode('utf-8'))

        # Ensure the request is an HTTP request
        if b'HTTP' not in request_line:
            # Invalid request
            print('Invalid request: {}'.format(request_line.decode('utf-8')))
            return
        
        # Split the request into separate components
        # 0 = GET/POST; 1 = URL path (e.g. /); 2 = HTTP prototype (e.g. HTTP/1.1)
        request_header = request_line.decode('utf-8').split(' ')

        # Initialize the response object
        resp = Response()

        if request_header[0] == 'GET':
            # Ignore remaining request header information
            while await sreader.readline() != b'\r\n':
                pass
            
            # Process the get request
            resp.get(request_header[1])
        
        elif request_header[0] == 'POST':
            # Use the header to determine the content length of the body
            line = ''
            content_length = 0
            while line != b'\r\n':
                line = await sreader.readline()
                if b'Content-Length' in line:
                    kv = line.decode('utf-8').split(': ')
                    content_length = int(kv[1])
                
                # Debugging line
                #print(line.decode('utf-8'))
            
            # Read the desired number of bytes
            if content_length > 0:
                # Read in the content
                post_body = await sreader.read(content_length)
                
                # Split the post into a dictionary of key value pairs
                post_content = post_body.decode('utf-8').split('&')
                post_kv = dict(x.split('=') for x in post_content)

                # Convert any URL encoded special characters back to special characters
                for k, v in post_kv.items():
                    new_v = v
                    while '%' in new_v:
                        idx = new_v.index('%') + 1
                        code = new_v[idx:idx+2]
                        char = chr(int(code,16))
                        new_v = new_v.replace(f'%{code}',char)
                    post_kv[k] = new_v
                    
            else:
                post_kv = {}
            
            # Take action based on request
            resp.post(request_header[1], post_kv)
                
        else:
            # Unknown get request, respond with an error
            resp.http_status = 400
            resp.body = f'<p>Invalid HTTP request type: {request_header[0]}</p><p>Return to the <a href="/">Home Page</a></p>'

        # Write the HTTP header and HTML
        swriter.write(self._http_header(status_code=resp.http_status))
        swriter.write(self._html_header())
        swriter.write(resp.body)
        swriter.write(self._html_footer())
        await swriter.drain()
        await swriter.wait_closed()

        if resp.exit_config:
            # Set the exit event
            self.event_config_exit.set()

    
    def _http_header(self, status_code=200, content_length=None ):
        """
        Response header to send to a client connection for the web server
        """
        html = f"HTTP/1.0 {status_code} OK\r\n"
        html += "Content-Type: text/html\r\n"
        if content_length is not None:
            html += f"Content-Length: {content_length}\r\n"
        html += "\r\n"

        return html
    
    def _html_header(self):
        """
        Return the standard HTML header tags
        """
        html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Clock Configuration</title>
            </head>
            <body>
            <h1>Clock Configuration</h1>
        """
        return html

    def _html_footer(self):
        """
        Return the standard closing HTML tags
        """
        return "</body></html>"
    
