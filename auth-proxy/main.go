package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"strings"
	"time"

	"github.com/gorilla/mux"
	"github.com/lestrrat-go/jwx/jwk"
	"github.com/lestrrat-go/jwx/jwt"
)

type AuthService struct {
	jwksUrl       string
	autoRefresher *jwk.AutoRefresh
}

func (authService *AuthService) Auth(responseWriter http.ResponseWriter, request *http.Request) {
	authorizationHeader := request.Header.Get("Authorization")
	authHeaderParts := strings.Split(authorizationHeader, " ")
	if len(authHeaderParts) != 2 {
		log.Println("Header is malformed.")
		responseWriter.WriteHeader(500)
		return
	}

	token := authHeaderParts[1]

	set, err := authService.autoRefresher.Fetch(context.Background(), authService.jwksUrl)

	if err != nil {
		log.Printf("failed to parse JWK: %s", err)
		responseWriter.WriteHeader(403)
		return
	}

	_, err = jwt.Parse([]byte(token), jwt.WithKeySet(set))
	if err != nil {
		log.Printf("failed to parse and validate token: %s", err)
		responseWriter.WriteHeader(403)
		return
	}

}

func main() {
	var exists bool
	jwksUrl, exists := os.LookupEnv("JWKS_URL")
	if !exists {
		jwksUrl = "https://philipp-lein.eu.auth0.com/.well-known/jwks.json"
	}
	log.Printf("using jwks url %s", jwksUrl)

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	autoRefresher := jwk.NewAutoRefresh(ctx)
	autoRefresher.Configure(jwksUrl, jwk.WithMinRefreshInterval(15*time.Minute))
	_, err := autoRefresher.Refresh(ctx, jwksUrl)
	if err != nil {
		log.Printf("failed to refresh JWKS: %s\n", err)
		os.Exit(1)
	}

	authService := AuthService{
		jwksUrl:       jwksUrl,
		autoRefresher: autoRefresher,
	}

	router := mux.NewRouter()
	router.PathPrefix("").Handler(http.HandlerFunc(authService.Auth))
	err = http.ListenAndServe(":9090", router)
	if err != nil {
		log.Printf("failed to start router: %s\n", err)
		return
	}
}
