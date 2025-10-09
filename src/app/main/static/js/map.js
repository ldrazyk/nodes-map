


const SvgMap = function () {
    
    let nodes, spec;
    let svg, container;
    const width = 1600, height = 700;
    
    const changeSvgBackground = function () {
        
        document.getElementById("map").style.backgroundColor = "hsla(78, 69%, 69%, 1.00)";
    };

    const fetchMapExample = async function (mapId) {
        
        const response = await fetch(`http://localhost:3000/api/map?id=${mapId}`);
        
        return await response.json();
    };

    const initSvg = function () {

        svg = d3.select("svg");
        container = svg.append("g");
    };

    const updateMap = async function () {

        const updateSvg = function (nodes) {
            
            const buildScales = function () {

                const xExtent = d3.extent(nodes, d => d.x);
                const yExtent = d3.extent(nodes, d => d.y);
    
                const xScale = d3.scaleLinear()
                    .domain(xExtent)        // input (UMAP coords)
                    .range([0, width]);     // output (SVG pixels)
    
                const yScale = d3.scaleLinear()
                    .domain(yExtent)
                    .range([height, 0]);    // flip y axis

                return [xScale, yScale];
            };

            const [xScale, yScale] = buildScales();

            const g = container.selectAll("g.node")
                .data(nodes, d => d.id)
                .enter()
                .append("g")
                .attr("class", "node")
                .attr("id", d => d.id)
                .attr("transform", d => `translate(${xScale(d.x)}, ${yScale(d.y)})`);
            
            g.append("text")
                .attr("class", "label")
                .text(d => d.label);
        };

        const updateInfo = function (spec) {

            document.getElementById("mapName").textContent = spec["map_name"];
        };
        
        const mapId = document.querySelector("head").dataset.mapid;

        const map = await fetchMapExample(mapId);
        nodes = map.nodes;
        spec = map.spec;
        console.log(nodes);
        console.log(spec);
        updateSvg(nodes);
        updateInfo(spec);

        const zoom = d3.zoom()
            .scaleExtent([0.5, 10]) // min and max zoom
            .on("zoom", (event) => {
                container.attr("transform", event.transform);
            });

        svg.call(zoom);
    };

    
    const init = async function () {

        initSvg();

        changeSvgBackground();

        updateMap();


    }();


    return Object.freeze(
        {

        }
    );
};


const main = async function () {
    
    console.log("This is map script...");
    
    
    const svgMap = SvgMap();
    
    
}();