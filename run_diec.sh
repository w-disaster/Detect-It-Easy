
docker run --rm \
    -v ~/MNTPOINT/SAMPLES/chunk:/usr/dataset/chunk:ro \
    -v ~/MNTPOINT/SAMPLES/malpe:/usr/dataset/malpe:ro \
    -v ~/MNTPOINT/SAMPLES/dotnet:/usr/dataset/dotnet:ro \
    -v ./diec-packing-results/:/usr/results/ \
    -e N_PROC=80 \
    diec-packing