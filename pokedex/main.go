package main

import (
	"time"

	"github.com/arockett/boot.dev/pokedex/internal/pokeapi"
)

func main() {
	cfg := &config{
		pokeapi: pokeapi.NewClient(5 * time.Second),
		pokedex: make(map[string]pokeapi.GetPokemonResp),
	}
	startRepl(cfg)
}
