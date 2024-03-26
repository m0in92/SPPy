import Plot from 'react-plotly.js';
function RenderDataPoints(props) {
    // both args are key-valued {"key": value}
    let xValue;
    let xKey;
    let yValue;
    let yKey;
    Object.entries(props.xVal).map(([key,value]) => {
        xKey = key;
        xValue = value;
    });
    Object.entries(props.yVal).map(([key,value]) => {
        yKey = key;
        yValue = value;
    });
    return(
        <Plot
        data={[
          {
            x: xValue,
            y: yValue,
            type: 'scatter',
            mode: 'lines',
            line: {
                  color: 'rgb(219, 64, 82)',
                  width: 3
            },
          },
        ]}
        layout={{
                width: 500,
                length: 500,
                plot_bgcolor: 'rgb(0, 0, 0, 0)',
                paper_bgcolor: 'rgb(0, 0, 0, 0)',
                margin: {
                    t: 25, //top margin
                    l: 45, //left margin
                    r: 45, //right margin,
                    b: 45 //bottom margin}
                },
                yaxis: {
                    autorange: true,
                    showgrid: true,
                    showline: true,
                    mirror: 'ticks',
                    gridwidth: 1,
                    tickfont: {
                        size: 14
                    },
                    title: {
                        text: yKey
                    },
                },
                xaxis: {
                    tickfont: {
                        size: 14
                    },
                    title: {
                        text: xKey,
                        font: {
                            size: 14
                        }
                    },
                    showline: true,
                    mirror: 'ticks',
                }
            }}
      />
    );
}

export default RenderDataPoints;