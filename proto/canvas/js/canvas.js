const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");

const testDrawRect = function () {

    ctx.fillStyle = "hsl(0, 90%, 60%)";
    ctx.fillRect(10, 10, 100, 100);
};


const Nodes = function (spec) {

    const { imgRoot, nodes } = spec;
    let nodesArea;

    const getNodesArea = function () {

        let min_x = 999999999999; 
        let min_y = min_x;
        let max_x = 0;
        let max_y = 0;

        for (let node of nodes) {
            if (node.x < min_x) {
                min_x = node.x;
            }
            if (node.y < min_y) {
                min_y = node.y;
            }
            if (node.x > max_x) {
                max_x = node.x;
            }
            if (node.y > max_y) {
                max_y = node.y;
            }
        }

        return [[min_x, max_x], [min_y, max_y]]
    };

    const init = function () {

        nodesArea = getNodesArea();
        console.log(nodesArea);
    }();
    
    const drawNodes = function () {
    
        const drawNode = function (node) {
            
            const drawImage = function () {
    
                const img = new Image();
                img.src = imgRoot + node.image;
                ctx.drawImage(img, node.x, node.y, 48, 48);
            };
    
            const printLabel = function () {
    
                ctx.font = "16px Arial";
                ctx.fillStyle = "white";
                ctx.fillText(node.label, node.x, node.y + 65);
            };
    
            drawImage();
            printLabel();
        };
        
        for (let node of nodes) {
            drawNode(node);
        };
    };

    return Object.freeze(
        {
            drawNodes,
        }
    )

};

const main = function () {

    const imgRoot = "img/"
    const nodesSpec = [
        {label: "Poland", x: 800, y: 150, image: "POL.png"},
        {label: "Russia", x: 1000, y: 100, image: "RUS.png"},
        {label: "China", x: 1300, y: 300, image: "CHN.png"},
        {label: "USA", x: 300, y: 300, image: "USA.png"},
        {label: "Kanada", x: 250, y: 100, image: "CAN.png"},
        {label: "Brasil", x: 400, y: 500, image: "BRA.png"},
    ];

    const nodes = Nodes({nodes: nodesSpec, imgRoot});
    nodes.drawNodes();

}();

