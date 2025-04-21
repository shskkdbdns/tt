#!/bin/bash

# List of proxies (IP:PORT:USER:PASS)
proxies=(
"38.153.152.244:9594:wwzneveb:sbwtjej8grv5"
"86.38.234.176:6630:wwzneveb:sbwtjej8grv5"
"173.211.0.148:6641:wwzneveb:sbwtjej8grv5"
"161.123.152.115:6360:wwzneveb:sbwtjej8grv5"
"216.10.27.159:6837:wwzneveb:sbwtjej8grv5"
"154.36.110.199:6853:wwzneveb:sbwtjej8grv5"
"45.151.162.198:6600:wwzneveb:sbwtjej8grv5"
"185.199.229.156:7492:wwzneveb:sbwtjej8grv5"
"185.199.228.220:7300:wwzneveb:sbwtjej8grv5"
"185.199.231.45:8382:wwzneveb:sbwtjej8grv5"
)

# Function to check if a proxy is working
check_proxy() {
    local proxy=$1
    IFS=':' read -r ip port user pass <<< "$proxy"
    result=$(curl -s -o /dev/null -w "%{http_code}" -x http://$user:$pass@$ip:$port http://ifconfig.me)

    if [ "$result" -eq 200 ]; then
        echo "$proxy is working"
        return 0
    else
        echo "$proxy is not working"
        return 1
    fi
}

# Function to select a working proxy
get_working_proxy() {
    # Randomly shuffle proxies array
    shuffled_proxies=($(shuf -e "${proxies[@]}"))
    for proxy in "${shuffled_proxies[@]}"; do
        if check_proxy "$proxy"; then
            echo "$proxy"
            return
        fi
    done
    echo "No working proxies found!"
    exit 1
}

# Function to rotate proxies every 1 hour
rotate_proxies() {
    # Infinite loop to rotate every hour
    while true; do
        # Get a working proxy
        selected_proxy=$(get_working_proxy)

        # Split into parts
        IFS=':' read -r ip port user pass <<< "$selected_proxy"

        # Export proxy environment variables
        export http_proxy="http://$user:$pass@$ip:$port"
        export https_proxy="http://$user:$pass@$ip:$port"

        # Show the current proxy being used
        echo "Using proxy: $ip:$port"

        # Wait for 1 hour (3600 seconds) before rotating to the next proxy
        sleep 600
    done
}

# Start the proxy rotation in the background
nohup bash -c 'rotate_proxies' &

# Wait for a moment to ensure the proxy is set
sleep 5

# Export proxy environment variables for Python
export http_proxy=$http_proxy
export https_proxy=$https_proxy

# Run your Python script with the proxy settings
echo "Running Python script with proxy..."
python3 y.py
