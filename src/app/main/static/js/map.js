

const NodesMap = function () {
    
    let nodes, spec;
    let mediator;

    const init = async function () {

        const fetchMap = async function (mapId) {
            
            const response = await fetch(`http://localhost:3000/api/map?id=${mapId}`);
            
            return await response.json();
        };

        const mapId = document.querySelector("head").dataset.mapid;
        const map = await fetchMap(mapId);
        nodes = map.nodes;
        spec = map.spec;
        console.log(nodes);
        console.log(spec);

    };


    const setMediator = function (newMediator) {

        mediator = newMediator;
    };

    const getNodes = function () {

        return nodes;
    };

    const getSpec = function () {

        return spec;
    };
    
    return Object.freeze(
        {
            init,
            setMediator,
            getNodes,
            getSpec,
        }
    );
};

const MapTranslator = function (spec) {

    const [[[minX0, maxX0], [minY0, maxY0]], [[minX1, maxX1], [minY1, maxY1]]] = spec;
    let scale, centerX0, centerY0, translationX, translationY;

    const init = function () {

        const getScale = function () {

            const width0 = Math.abs(maxX0 - minX0);
            const width1 = Math.abs(maxX1 - minX1);
            const height0 = Math.abs(maxY0 - minY0);
            const height1 = Math.abs(maxY1 - minY1);

            const proportion0 = width0 / height0;
            const proportion1 = width1 / height1;

            const widthScale = width1 / width0;
            const heightScale = height1 / height0;

            if (proportion1 > proportion0) {
                return heightScale;
            } else {
                return widthScale;
            };
        };

        scale = getScale();
        centerX0 = (minX0 + maxX0) / 2;
        centerY0 = (minY0 + maxY0) / 2;
        const centerX1 = (minX1 + maxX1) / 2;
        const centerY1 = (minY1 + maxY1) / 2;
        translationX = centerX1 - centerX0;
        translationY = centerY1 - centerY0;
    }();

    const translateCoordinate = function (coordinate, centerCoordinate0, scale, translation) {


        const scaleCoordinate = function (coordinate, centerCoordinate, scale) {
                
                return centerCoordinate + (coordinate - centerCoordinate) * scale;
            };

            const translateCoordinate = function (coordinate, translation) {

                return coordinate + translation;
            };

            return translateCoordinate(scaleCoordinate(coordinate, centerCoordinate0, scale), translation);
        };

    const translateX = function (x) {

        return translateCoordinate(x, centerX0, scale, translationX);
    };

    const translateY = function (y) {

        return translateCoordinate(y, centerY0, scale, translationY);
    };

    const getScale = function () {

        return scale;
    };

    return Object.freeze(
        {
            translateX,
            translateY,
            getScale,
        }
    );
};

const SvgMap = function () {
    
    let svg, container;
    const minZoom = 0.5;
    const maxZoom = 1000;
    let mediator;

    const initSvg = function () {

        svg = d3.select("svg");
        container = svg.append("g");
    };
    
    const changeSvgBackground = function () {
        
        document.getElementById("map").style.backgroundColor = "hsla(78, 69%, 69%, 1.00)";
    };

    const addZoom = function () {

        const zoom = d3.zoom()
            .scaleExtent([minZoom, maxZoom])
            .on("zoom", (event) => {
                container.attr("transform", event.transform);
            });

        svg.call(zoom);
    };

    const init = function () {
        
        initSvg();
        changeSvgBackground();
        addZoom();
    }();

    const setMediator = function (newMediator) {

        mediator = newMediator;
    };

    const update = function () {

        const updateSvg = function (nodesData) {

            let maxSize;

            const getMapTranslator = function () {

                const xExtent = d3.extent(nodesData, d => d.x);
                const yExtent = d3.extent(nodesData, d => d.y);
                const translatorSpec = [
                    [[xExtent[0], xExtent[1]], [yExtent[0], yExtent[1]]],
                    [[50, 1550], [50, 650]]
                ];
                return MapTranslator(translatorSpec);
            };

            const getMaxSize = function (scale) {

                const getDistances = function () {
    
                    const distances = [];
                    
                    const nodesNumber = nodesData.length;

                    for (let i = 0; i < nodesNumber; i++) {
                        for (let j = 0; j < nodesNumber; j++) {
                            if (i != j) {
                                const dx = nodesData[i].x - nodesData[j].x;
                                const dy = nodesData[i].y - nodesData[j].y;
                                distances.push(Math.sqrt(dx*dx + dy*dy));
                            }
                        }
                    }
    
                    return distances;
                };

                const distances = getDistances();
                const closeNodesFraction = 0.13;
                const quantileLevel = closeNodesFraction / nodesData.length;
                const quantile = d3.quantile(distances, quantileLevel);
                const min = d3.min(distances);
                const maxSize = quantile * scale / 1.4;

                console.log(`nodes.length: ${nodesData.length}`);
                console.log(`30 / nodes.length: ${30 / nodesData.length}`);
                console.log(`min: ${min}`);
                console.log(`quantileLevel: ${quantileLevel}`);
                console.log(`quantile: ${quantile}`);
                console.log(`maxSize: ${maxSize}`);

                return maxSize;
            };

            const createNodes = function (translator) {

                const nodes = container.selectAll("g.node")
                    .data(nodesData, d => d.id)
                    .enter()
                    .append("g")
                    .attr("class", "node")
                    .attr("id", d => d.id)
                    .attr("transform", d => `translate(${translator.translateX(d.x)}, ${translator.translateY(d.y)})`);

                return nodes
            };

            const getSize = function (d) {

                const scale = d.size || 1;
                                
                return scale * maxSize;
            };
                
            const addRects = function (nodes) {
                
                const getX = function (d) {
    
                    return -getSize(d) / 2;
                };
    
                const getY = getX;

                nodes.append("rect")
                    .attr("x", getX)
                    .attr("y", getY)
                    .attr("width", getSize)
                    .attr("height", getSize);


                if (nodesData[0].image) {
                    
                    nodes.append("image")
                        .attr("xlink:href", d => d.image)
                        .attr("x", getX)
                        .attr("y", getY)
                        .attr("width", getSize)
                        .attr("height", getSize);
                }                
            };

            const addLabels = function (nodes) {

                nodes.append("text")
                    .attr("class", "label")
                    .attr("y", d => getSize(d) * 1.0)
                    .attr("font-size", maxSize * 0.5)
                    .attr("text-anchor", "middle")
                    .text(d => d.label || d.id);
            };

            const translator = getMapTranslator();
            maxSize = getMaxSize(translator.getScale());
            const nodes = createNodes(translator);
            addRects(nodes);
            addLabels(nodes);
            
        };

        const updateInfo = function (mapSpec) {

            document.getElementById("mapName").textContent = mapSpec["map_name"];
        };

        const nodesData = mediator.getNodes();
        const mapSpec = mediator.getMapSpec();
        
        updateSvg(nodesData);
        updateInfo(mapSpec);
    };


    return Object.freeze(
        {
            setMediator,
            update,
        }
    );
};

const Menu = function () {
    
    let nodeSelect;
    let mediator;

    const init = function () {

        nodeSelect = document.getElementById("nodeSelect");

    }();

    const setMediator = function (newMediator) {

        mediator = newMediator;
    };

    const update = function () {

        const addNodeSelectOptions = function (nodes) {

            const createOption = function (node) {
                
                const option = document.createElement('option');
                option.value = node.id;
                option.textContent = node.label ?? node.id;
                return option;
            };

            const compareTextContent = function (a, b) {

                a = a.textContent;
                b = b.textContent;

                if (a == b) {
                    return 0;
                } else if (a < b) {
                    return -1;
                } else {
                    return 1;
                }
            };
            
            const optionElements = [];
            
            for (let node of nodes) {
                optionElements.push(createOption(node));
            }

            optionElements.sort(compareTextContent);
            
            for (let option of optionElements) {
                nodeSelect.appendChild(option);
            }
        };


        const nodes = mediator.getNodes();
        addNodeSelectOptions(nodes);
    };
    
    
    return Object.freeze(
        {
            setMediator,
            update,
        }
    );
};

const Mediator = function () {
    
    let nodesMap, svgMap, menu;
    
    const setNodesMap = function (newNodesMap) {

        nodesMap = newNodesMap;
    };
    
    const setSvgMap = function (newSvgMap) {

        svgMap = newSvgMap;
    };
    
    const setMenu = function (newMenu) {

        menu = newMenu;
    };

    const getNodes = function () {

        return nodesMap.getNodes();
    };

    const getMapSpec = function () {

        return nodesMap.getSpec();
    };
    
    return Object.freeze(
        {
            setNodesMap,
            setSvgMap,
            setMenu,
            getNodes,
            getMapSpec,
        }
    );
};

const build = async function () {

    let nodesMap, svgMap, menu;
    let mediator;

    const setMediator = function () {

        mediator = Mediator();
        mediator.setNodesMap(nodesMap);
        mediator.setSvgMap(svgMap);
        mediator.setMenu(menu);
        
        for (let component of [nodesMap, svgMap, menu]) {
            component.setMediator(mediator);
        }
    };

    nodesMap = NodesMap();
    await nodesMap.init();

    svgMap = SvgMap();
    menu = Menu();
    
    setMediator();

    for (let component of [svgMap, menu]) {
        component.update();
    }
};


const main = function () {
    
    console.log("This is map script...");
    
    build();
    
}();