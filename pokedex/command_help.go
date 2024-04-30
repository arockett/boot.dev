package main

import "fmt"

func commandHelp(cfg *config, args ...string) error {
	fmt.Println()
	fmt.Println("Welcome to the Pokedex!")
	fmt.Println("Usage:")
	fmt.Println()
	for cmdName, cmd := range getCommands() {
		fmt.Printf("%s: %s\n", cmdName, cmd.description)
	}
	fmt.Println()
	return nil
}
