package pokeapi

import (
	"encoding/json"
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

	body, err := c.CachedGet(url)
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
