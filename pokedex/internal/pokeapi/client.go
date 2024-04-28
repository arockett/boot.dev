package pokeapi

import (
	"fmt"
	"io"
	"net/http"
	"time"

	"github.com/arockett/boot.dev/pokedex/internal/pokecache"
)

type Client struct {
	httpClient http.Client
	cache      pokecache.Cache
}

func NewClient(timeout time.Duration) Client {
	return Client{
		httpClient: http.Client{
			Timeout: timeout,
		},
		cache: pokecache.NewCache(5 * time.Minute),
	}
}

func (c *Client) CachedGet(url string) ([]byte, error) {
	if val, cached := c.cache.Get(url); cached {
		return val, nil
	}
	res, err := c.httpClient.Get(url)
	if err != nil {
		return nil, err
	}
	body, err := io.ReadAll(res.Body)
	defer res.Body.Close()
	if res.StatusCode > 299 {
		return nil, fmt.Errorf("GET %s failed with status code: %d", url, res.StatusCode)
	}
	if err != nil {
		return nil, err
	}
	c.cache.Add(url, body)
	return body, nil
}
