package main

import (
	"time"

	"github.com/arockett/boot.dev/pokedex/internal/pokeapi"
)

func main() {
	cfg := &config{
		pokeapi: pokeapi.NewClient(5 * time.Second),
	}
	startRepl(cfg)
}
