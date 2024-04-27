package pokeapi

import (
	"encoding/json"
	"fmt"
	"io"
)

type ListLocationsResp struct {
	Count    int     `json:"count"`
	Next     *string `json:"next"`
	Previous *string `json:"previous"`
	Results  []struct {
		Name string `json:"name"`
		URL  string `json:"url"`
	} `json:"results"`
}

func (c *Client) ListLocations(pageUrl *string) (ListLocationsResp, error) {
	url := baseUrl + "/location-area"
	if pageUrl != nil {
		url = *pageUrl
	}

	res, err := c.httpClient.Get(url)
	if err != nil {
		return ListLocationsResp{}, err
	}
	body, err := io.ReadAll(res.Body)
	defer res.Body.Close()
	if res.StatusCode > 299 {
		return ListLocationsResp{}, fmt.Errorf("ListLocations failed with status code: %d", res.StatusCode)
	}
	if err != nil {
		return ListLocationsResp{}, err
	}

	listResp := ListLocationsResp{}
	err = json.Unmarshal(body, &listResp)
	if err != nil {
		return ListLocationsResp{}, err
	}

	return listResp, nil
}
