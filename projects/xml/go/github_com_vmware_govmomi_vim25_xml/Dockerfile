FROM --platform=linux/arm64 golang@sha256:8d48e12ec56735e9358640898b9d9b9fcca110612ed8a5567438c0a1baa24e66 AS build
WORKDIR /work
COPY go.mod go.sum ./
RUN go mod download github.com/vmware/govmomi@v0.56.2 \
    && echo '195de21afbe5a372c5afedcc59fef87cec96d07e9564cecf50e037fa31d079d4  /go/pkg/mod/cache/download/github.com/vmware/govmomi/@v/v0.56.2.zip' | sha256sum --check \
    && echo '31e0058c75b46ec196c3cf2b55c1f867ee110f8f0de7eaf007e169af02b09119  /go/pkg/mod/github.com/vmware/govmomi@v0.56.2/vim25/xml/xml.go' | sha256sum --check \
    && echo '2d36597f7117c38b006835ae7f537487207d8ec407aa9d9980794b2030cbc067  /go/pkg/mod/github.com/vmware/govmomi@v0.56.2/vim25/xml/LICENSE' | sha256sum --check
COPY harness.go harness_test.go ./
RUN CGO_ENABLED=0 go test -c -coverpkg=github.com/vmware/govmomi/vim25/xml -o /work/harness.test .
COPY reporter/main.go ./reporter/main.go
RUN CGO_ENABLED=0 go build -o /work/reporter-bin ./reporter
FROM scratch
COPY --from=build /work/harness.test /work/harness.test
COPY --from=build /work/reporter-bin /work/reporter
ENTRYPOINT ["/work/reporter"]
