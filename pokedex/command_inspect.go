package main

import "fmt"

func commandInspect(cfg *config, args ...string) error {
	if len(args) == 0 {
		return fmt.Errorf("Missing pokemon name")
	}
	pokemonName := args[0]
	pokemon, caught := cfg.pokedex[pokemonName]
	if !caught {
		fmt.Printf("you have not caught a %s\n", pokemonName)
	} else {
		fmt.Printf("Name: %s\n", pokemon.Name)
		fmt.Printf("Height: %d\n", pokemon.Height)
		fmt.Printf("Weight: %d\n", pokemon.Weight)
		fmt.Println("Stats:")
		for _, stat := range pokemon.Stats {
			fmt.Printf("  -%s: %d\n", stat.Stat.Name, stat.BaseStat)
		}
		fmt.Println("Types:")
		for _, typ := range pokemon.Types {
			fmt.Printf("  - %s\n", typ.Type.Name)
		}
	}
	return nil
}
