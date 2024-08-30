from bokeh.plotting import figure, show, output_notebook
from bokeh.models import ColumnDataSource, HoverTool, BoxSelectTool, CustomJS, Slider
from bokeh.layouts import column, row
from bokeh.models.widgets import Div, Button
from IPython.display import display, HTML
from bokeh.transform import factor_mark
from bokeh.models import Legend, LegendItem

def RISE_tool(
        coordinates_list,
        image_paths,
        predictions,
        colours, 
        DR_techniques = ["T-SNE", "PCA", "FeatureAgglomeration", "IsoMap", "UMap"],
        markers = None,
        
    ):

    # Create a ColumnDataSource
    dummy_markers = ["circle" for i in range(len(image_paths))]
    source = ColumnDataSource(data=dict(x=coordinates_list[0]['x'], y=coordinates_list[0]['y'], images=image_paths, colours=colours, predictions = predictions, markers=markers if markers is not None else dummy_markers))

    # Create a figure
    p = figure(width=600, height=500, tools="")

    # Add scatter renderer
    p.scatter('x', 'y', size=5, source=source, color = "colours", marker = "markers")

    # Create legends
    color_legend_items = [
        LegendItem(label = "Predictions"),
        LegendItem(label="Wildlife", renderers=[p.circle([1], [1], color='red', visible=False)]),
        LegendItem(label="Domestic Dog", renderers=[p.circle([1], [1], color='green', visible=False)]),
        LegendItem(label="Domestic Cat", renderers=[p.circle([1], [1], color='blue', visible=False)])
    ]

    if markers is not None:
        marker_legend_items = [
        LegendItem(label = ""),
        LegendItem(label = "Human Labels"),
        LegendItem(label="Wildlife", renderers=[p.square([1], [1], color='black', visible=False)]),
        LegendItem(label="Domestic Dog", renderers=[p.circle([1], [1], color='black', visible=False)]),
        LegendItem(label="Domestic Cat", renderers=[p.triangle([1], [1], color='black', visible=False)])
        ]

        color_legend_items += marker_legend_items

    legend = Legend(items=color_legend_items)

    p.add_layout(legend, 'right')
    
    # Create a HoverTool with custom HTML to display the image
    hover = HoverTool(tooltips="""
        <div>
            <div>
                <img
                    src="@images" height="100" alt="@images" width="100"
                    style="float: left; margin: 0px 0px 0px 0px;"
                    border="0px"
                ></img>
            </div>
        </div>
    """)

    # Add the hover tool to the figure
    p.add_tools(hover)

    # Add a BoxSelectTool to the figure
    box_select = BoxSelectTool()
    p.add_tools(box_select)

    # Create a Div to display the images
    div = Div(width=600)

    # CustomJS callback to update the Div with the selected images
    callback = CustomJS(args=dict(source=source, div=div), code="""
        const indices = source.selected.indices;
        let images = '';
        for (let i = 0; i < indices.length; i++) {
            const index = indices[i];
            images += `<img class="hover-enlarge" src="${source.data.images[index]}" height="150" alt="Image" width="150" style="margin: 5px; border: 2px solid ${source.data.colours[index]};"/>`;
        }
        div.text =  `<div style="height:550px;overflow:auto;">${images}</div>`;
    """)

    # Add the callback to the source's selected property
    source.selected.js_on_change('indices', callback)

    dr_div = Div(text=f"Dimensionality Reduction Technique: {DR_techniques[0]}", width=600, height=10)

    # Create Slider object 
    slider = Slider(start=0, end=len(coordinates_list)-1, value=0, 
                    step=1) 

    slider_callback = CustomJS(args=dict(source=source, coords_list=coordinates_list, val=slider, dr_div=dr_div, dr_techniques=DR_techniques), code="""
        source.data.x = coords_list[val.value].x;
        source.data.y = coords_list[val.value].y;
        dr_div.text = `Dimensionality Reduction Technique: ${dr_techniques[val.value]}`;
        source.change.emit();
    """)

    #enlarge images on hover
    display(HTML("""
    <style>
    .hover-enlarge:hover {
        transform: scale(1.4);
        position: relative;
    }
    </style>
    """))

    slider.js_on_change('value', slider_callback) 

    # Layout the plot, div, and button
    layout = row(column(p, dr_div, slider),div)

    # Show the plot
    show(layout)