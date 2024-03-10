FROM golang:1.19 AS builder

WORKDIR /app

COPY go.mod ./
COPY go.sum ./

RUN go mod download

COPY . .

RUN go build -o /go/bin/app

FROM gcr.io/distroless/base

EXPOSE 9090
COPY --from=builder /go/bin/app /app

ENTRYPOINT ["/app"]