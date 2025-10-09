# Architecture

## 1. Ui Forms

### Create Map Form

`form` -> [Create Map Api Route](#2-create-map-api-route) ->  [Show Map Page](#5-show-map-page)

**Params**:

|Form Name|Spec Key|Type|Default|Spec Dict|Application|
|---|---|---|---|---|---|
|mapName|map_name|str|“”|-|store_map()|
|specSrc|url|str|“”|api|get_nodes_spec()|
|specId|id|str|“”|api|get_nodes_spec()|
|scaleFeatures|scale_features|bool|False|preprocess|scale_features()|
|normalize|normalize|bool|False|preprocess|normalize_embeddings()|
|reduce|reduce|bool|False|preprocess|reduce_embeddings()|
|normalizeReduceInput|normalize_reduce_input|bool|True|preprocess|reduce_embeddings()|
|reductionSize|reduction_size|int|64|preprocess|reduce_embeddings()|
|normalizeReduceOutput|normalize_reduce_output|bool|True|preprocess|reduce_embeddings()|
|combine|combine|bool|False|preprocess|combine_embeddings()|
|normalizeCombineInput|normalize_combine_input|bool|True|preprocess|combine_embeddings()|
|inputReductionSize|input_reduction_size|int|64|preprocess|combine_embeddings()|
|outputReductionSize|output_reduction_size|int|128|preprocess|combine_embeddings()|
|normalizeCombineOutput|normalize_combine_output|bool|True|preprocess|combine_embeddings()|
|cluster|cluster|bool|True|mapping|create()|
|minCluster|min_cluster|int|0|mapping|create()|
|maxCluster|max_cluster|int|0|mapping|create()|
|metric|metric|str|cosine|mapping|create()|
|nNeighbors|n_neighbors|int|3|mapping|create()|
|randomState|random_state|int|22|mapping|create()|
|minDistance|min_distance|float|0.1|mapping|create()|
|spread|spread|float|1.0|mapping|create()|

### Show Map Form

`mapId` -> [Show Map Page](#5-show-map-page)

## 2. Create Map Api Route

Route to create map in model from form and show the map.

`request.form` -> `spec` -> [Create Map in Model](#3-create-map-in-model) -> `mapId` -> [Show Map Page](#5-show-map-page)

- function: `api.create_map`
- url: `/api/map/create`
- metode: POST
- returns: redirect to [Show Map Page](#5-show-map-page)

## 3. Create Map in Model

### Get Nodes Spec

### Preprocess Embeddings

### Create Map

### Store Map

## 4. Nodes Spec External Api Route

## 5. Show Map Page

Route to show map with `mapId` using D3.js

- function: `main.show_map`
- url: `/map`
- metode: GET
- args: `mapId`
- returns: render map page

Map is fetched from [Get Map Api Route](#6-get-map-api-route).

## 6. Get Map Api Route

Route to fetch map.
