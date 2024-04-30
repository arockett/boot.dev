package main

import "fmt"

func commandExplore(cfg *config, args ...string) error {
	if len(args) == 0 {
		return fmt.Errorf("Missing location name")
	}
	locationName := args[0]
	fmt.Printf("Exploring %s...\n", locationName)
	resp, err := cfg.pokeapi.GetLocation(locationName)
	if err != nil {
		return err
	}
	fmt.Println("Found Pokemon:")
	for _, encounter := range resp.PokemonEncounters {
		fmt.Println(" - " + encounter.Pokemon.Name)
	}
	return nil
}
