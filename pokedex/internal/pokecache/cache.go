package pokecache

import (
	"sync"
	"time"
)

type cacheEntry struct {
	createdAt time.Time
	val       []byte
}

type Cache struct {
	entries map[string]cacheEntry
	mu      *sync.Mutex
}

func NewCache(reapInterval time.Duration) Cache {
	cache := Cache{
		entries: make(map[string]cacheEntry),
		mu:      &sync.Mutex{},
	}
	go cache.reapLoop(reapInterval)
	return cache
}

func (c *Cache) Add(key string, val []byte) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.entries[key] = cacheEntry{
		createdAt: time.Now(),
		val:       val,
	}
}

func (c *Cache) Get(key string) ([]byte, bool) {
	c.mu.Lock()
	defer c.mu.Unlock()
	entry, exists := c.entries[key]
	return entry.val, exists
}

func (c *Cache) reapLoop(maxLifespan time.Duration) {
	timer := time.NewTimer(maxLifespan)
	for range timer.C {
		c.reap(time.Now(), maxLifespan)
	}
}

func (c *Cache) reap(now time.Time, maxLifespan time.Duration) {
	c.mu.Lock()
	defer c.mu.Unlock()
	for key, entry := range c.entries {
		lifespan := now.Sub(entry.createdAt)
		if lifespan > maxLifespan {
			delete(c.entries, key)
		}
	}
}
