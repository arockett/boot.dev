package main

import "fmt"

func commandMap(cfg *config, args ...string) error {
	resp, err := cfg.pokeapi.ListLocations(cfg.nextLocationsUrl)
	if err != nil {
		return err
	}
	cfg.prevLocationsUrl = resp.Previous
	cfg.nextLocationsUrl = resp.Next
	for _, loc := range resp.Results {
		fmt.Println(loc.Name)
	}
	return nil
}

func commandMapb(cfg *config, args ...string) error {
	if cfg.prevLocationsUrl == nil {
		return fmt.Errorf("Already at first page of locations")
	}
	cfg.nextLocationsUrl = cfg.prevLocationsUrl
	return commandMap(cfg)
}
