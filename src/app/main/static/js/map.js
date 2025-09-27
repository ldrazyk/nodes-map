


const SvgMap = function () {
    
    let nodes;
    let svg, container;
    const width = 1600, height = 700;
    
    const changeSvgBackground = function () {
        
        document.getElementById("map").style.backgroundColor = "hsla(78, 69%, 69%, 1.00)";
    };

    const fetchMapExample = async function (map_id) {
        
        const response = await fetch(
            "http://localhost:3000/api/map/example",
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ id: map_id })
            }
        );
        
        return await response.json();
    };

    const initSvg = function () {

        svg = d3.select("svg");
        container = svg.append("g");
    };

    const updateMap = async function () {

        const update = function (nodes) {
            
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
        
        const animals_id = "animals";
        const countries_id = "countries"

        nodes = await fetchMapExample(countries_id);
        console.log(nodes);
        update(nodes);

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