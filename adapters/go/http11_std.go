// Verify Go net/http parses local HTTP/1.1 request and response control bytes.
package main

import (
	"bufio"
	"encoding/json"
	"io"
	"net/http"
	"os"
	"strings"
)

func main() {
	if len(os.Args) != 3 {
		panic("usage: go run adapters/go/http11_std.go REQUEST_PATH RESPONSE_PATH")
	}
	requestBytes, err := os.ReadFile(os.Args[1])
	if err != nil {
		panic(err)
	}
	request, err := http.ReadRequest(bufio.NewReader(strings.NewReader(string(requestBytes))))
	if err != nil {
		panic(err)
	}
	defer request.Body.Close()
	responseBytes, err := os.ReadFile(os.Args[2])
	if err != nil {
		panic(err)
	}
	response, err := http.ReadResponse(bufio.NewReader(strings.NewReader(string(responseBytes))), request)
	if err != nil {
		panic(err)
	}
	defer response.Body.Close()
	body, err := io.ReadAll(response.Body)
	if err != nil {
		panic(err)
	}
	result := map[string]any{
		"request":  map[string]any{"method": request.Method, "target": request.RequestURI, "host": request.Host, "proto": request.Proto},
		"response": map[string]any{"status": response.StatusCode, "proto": response.Proto, "body": string(body)},
	}
	if err := json.NewEncoder(os.Stdout).Encode(result); err != nil {
		panic(err)
	}
}
