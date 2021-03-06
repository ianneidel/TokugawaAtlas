<template>
<div id="map">
  <div class="vld-parent" id="loadScreen"> 
    <loading :active.sync="isLoading" :is-full-page="fullPage"></loading> 
  </div>
   <div id="mapView">
    <screenshot :view="view" />
    <navbar @changeSettings="updateFilter"></navbar>
  </div>
</div>
</template>

<script>

import { loadModules, setDefaultOptions } from 'esri-loader';
import Screenshot from './Screenshot.vue';
import Navbar from './NewNavBar.vue';

import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/vue-loading.css';

import { bothrenderer } from './Both.js'
import { newcomerrenderer } from './Newcomer.js'
import { incumbentrenderer } from './Incumbent.js'

var domains; //declared since the update code precedes its initialization

export default {
  name: 'web-map',
  components: {
    Screenshot, 
    Loading,
    Navbar,
  },
  data(){
    return{
      view: null,
      isMounted: false,
      isLoading: true,
      fullPage: true,
      preferences: {
        domains: {
          branch: '',
          uncertainty: '',
          styling: '',
        },
        villages: '',
        guns: '',
      },
      layers:{},

      // Objects with feature layer meta data so mounted code does not have to change if data hosted elsewhere or data fields change
      layerInfo: {
        guns: {
          layer_name: "Guns",
          service_url: "https://services1.arcgis.com/7uJv7I3kgh2y7Pe0/arcgis/rest/services/Gun_Simple/FeatureServer/0",
          zoom_scale: 10000,
          fields: [
            { label: "Gun Name", id: "Dump_Gun_1", visible: true, search: true},
            { label: "Kuni Kanji",id: "Dump_Gun_3", visible: true, search: true},
            { label: "Kuni Romaji", id: "Dump_Gun_4", visible: true, search: true},
            { label: "Size", id: "Dump_Gun_S", visible: true, search: false},
            { label: "Year (Int)", id: "Year", visible: true, search: false},
            { label: "Check", id: "check_", visible: true, search: false},
            { label: "Start (int)", id: "START", visible: true, search: false},
            { label: "End (int)", id: "END_", visible: true, search: false},
            { label: "Year", id: "Year_dt	", visible: true, search: false},
            { label: "Start", id: "Start_dt", visible: true, search: false},
            { label: "End", id: "End_dt", visible: true, search: false},
          ],
        }, 
        villages: {
          layer_name: "Villages",
          service_url: "https://services1.arcgis.com/7uJv7I3kgh2y7Pe0/arcgis/rest/services/Villages_simp/FeatureServer/0",
          zoom_scale: 100000,
          fields: [
            { label: "Village Name", id: "Dump_Vil_1", visible: true, search: true},
            { label: "Year (Int)", id: "Year", visible: true, search: false},
            { label: "Start (int)", id: "START", visible: true, search: false},
            { label: "End (int)", id: "END_", visible: true, search: false},
            { label: "Start", id: "Start_dt", visible: true, search: false},
            { label: "End", id: "End_dt", visible: true, search: false},
          ],
        },
        domains: {
          layer_name: "Domains",
          service_url: "https://services1.arcgis.com/7uJv7I3kgh2y7Pe0/arcgis/rest/services/Domains_shape/FeatureServer/0",
          zoom_scale: 10000,
          fields: [
            { label: "Domain Kanji", id: "Dump_Dom_1", visible: true, search: true},
            { label: "Domain Size", id: "Dump_Dom_7", visible: true, search: false},
            { label: "Domain Family Kanji", id: "Dump_Dom_9", visible: true, search: true},
            { label: "Domain Aikyuu", id: "Dump_Dom11", visible: true, search: false},
            { label: "Domain Azukari", id: "Dump_Dom12", visible: true, search: false},
            { label: "Domain NI Situation", id: "Dump_Dom13", visible: true, search: false},
            { label: "Start (int)", id: "START", visible: true, search: false},
            { label: "End (int)", id: "END_", visible: true, search: false},
            { label: "Start", id: "Start_dt", visible: true, search: false},
            { label: "End", id: "End_dt", visible: true, search: false},
          ],
        },
        kunis: {
          layer_name: "Kunis",
          service_url: "https://services1.arcgis.com/7uJv7I3kgh2y7Pe0/arcgis/rest/services/Kuni/FeatureServer/0",
          zoom_scale: 10000,
          fields: [
            { label: "Kuni Kanji", id: "Dump_Gun_1", visible: true, search: true},
            { label: "Kuni Romaji", id: "Dump_Gun_2", visible: true, search: true},
            { label: "Start (int)", id: "START", visible: true, search: false},
            { label: "End (int)", id: "END_", visible: true, search: false},
            { label: "Start", id: "Start_dt", visible: true, search: false},
            { label: "End", id: "End_dt", visible: true, search: false},
          ],
        }

      }
        
      // Map data field names to generic names so code does not have to change when data representation does
      // Old data laters for Fukui only
      // gun_service_url: "https://services1.arcgis.com/7uJv7I3kgh2y7Pe0/arcgis/rest/services/Files_v4/FeatureServer/3?token=mmhhlZVuoCbYWtcVWcZ9AYOUdbomDLEBhIhLba3oMmu6qJx33R8bw-dH2d0f9W7XASmknv6VeIo4DSAvo9E2gRmaqqPxEljkvyf8ZQBRzOXeop6IruZkCdKvzIIX-QhISsuM7fNoztJbdYpnAL-Q2Au9F37giFIxaI1Z6BHG0kDLb9jUphpqxgVeNd5FOkzgogGuhIPBh8-AMTQ8RcsKHCQkxNbVG3GJZsXBMWmi1uqd4ndGnsR0Pn5riTgZEYV-",
    }
  },
  methods: {
    updateStyling(style){ return style; },
    updateFilter(form){
      console.log("New Settings:")
      console.log(form);
      if (form.domains.uncertainty == 'Both') { //could be improved by checking whether the uncertainty has been changed before updating the renderer
        domains.renderer = bothrenderer;
      } else if (form.domains.uncertainty == 'Newcomer') {
        domains.renderer = newcomerrenderer;
      } else {
        domains.renderer = incumbentrenderer;
      }
      console.log(form.domains.uncertainty);
    },

    /*
      Helper function to generate popups for feature layers.
    */
    genPopup(title, fields) {
      let fieldInfos = [];
      fields.forEach(field => {
        fieldInfos.push({
          fieldName: field.id,
          label: field.label,
          visible: field.visible
        })
      })

      // Return expected format for popup to autocast as FieldContent object
      return { 
        "title": `<b>${title}</b>`, 
        "content": [{
          type: "fields",
          fieldInfos: fieldInfos, 
        }],
      };
    }
  },
  mounted() {
    setDefaultOptions({version: '4.18'});

    // lazy load the required ArcGIS API for JavaScript modules and CSS
    loadModules([
      "esri/Map",
      "esri/views/MapView",
      "esri/core/watchUtils",
      "esri/layers/FeatureLayer",
      "esri/widgets/TimeSlider",
      "esri/widgets/LayerList",
      "esri/widgets/Legend",
      "esri/widgets/Search",
      "esri/widgets/Expand",
      "esri/widgets/BasemapGallery",
      "esri/widgets/Print",
      "esri/widgets/Print/TemplateOptions",
      ], { css: true })
    .then(([ArcGISMap, MapView, watchUtils, FeatureLayer, TimeSlider, LayerList, Legend, Search, Expand, BasemapGallery,
            Print, TemplateOptions]) => {
      
      /* =====================================  INITIALIZE MAP  ============================================= */

      const map = new ArcGISMap({ basemap: 'gray-vector' });
      this.view = new MapView({
        container: this.$el,
        map: map,
        center: [139.691706, 35.689487],
        zoom: 6,
        // scale: 4155583.4197442674,
      });

      /* =====================================   INIT LAYERS    ============================================= */

      let guns = new FeatureLayer({ 
        url: this.layerInfo.guns.service_url,
        popupTemplate: this.genPopup("Gun Information", this.layerInfo.guns.fields),
        outfields: ["*"],
      });
      
      let villages = new FeatureLayer({ 
        url: this.layerInfo.villages.service_url,
        popupTemplate: this.genPopup("Village Information", this.layerInfo.villages.fields),
        outfields: ["*"],
      });
      
      domains = new FeatureLayer({ 
        url: this.layerInfo.domains.service_url,
        popupTemplate: this.genPopup("Domain Information", this.layerInfo.domains.fields),
        renderer: bothrenderer,
        outfields: ["*"],
      });

      let kunis = new FeatureLayer({ 
        url: this.layerInfo.kunis.service_url,
        popupTemplate: this.genPopup("Kuni Information", this.layerInfo.kunis.fields),
        outfields: ["*"],
      });

      // Keep track of all the references to feature lyaers in our layerInfo object
      this.layers.guns = guns;
      this.layers.domains = domains;
      this.layers.villages = villages;
      this.layers.kunis = kunis;

      // Add all the feature layers to the map
      Object.values(this.layers).forEach((layer) => {
        map.layers.add(layer);
      })


      /* =====================================================================================================
                                          WIDGET CODE
      =======================================================================================================*/
    

      /*******************************************  
                Time Slider (Bottom Left)
      ********************************************/

      const timeSlider = new TimeSlider({
        container: "timeSlider",
        mode: "instant",
        view: this.view
      });

      // Add the time slider widget
      this.view.ui.add(timeSlider, "bottom-left");

      this.view.whenLayerView(villages).then(function() {
        const fullTimeExtent = villages.timeInfo.fullTimeExtent;

        // set up time slider properties
        timeSlider.fullTimeExtent = fullTimeExtent;
        timeSlider.stops = {
          interval: {
            value: 1,
            unit: "years"
          },
        };
        timeSlider.values =  [
          new Date(1700, 0, 1) // Initialize the current time for the beginning of the fullTimeExtent.
        ]
      });

      // // watch current time
      // timeSlider.watch("values", function(values){
      //   console.log("The current time is: ", values[0]);
      // });

      /*******************************************  
                Legend (Bottom Right)
      ********************************************/

      this.legendExpand = new Expand({
        view: this.view,
        expandIconClass: "esri-icon-polygon",  // see https://developers.arcgis.com/javascript/latest/guide/esri-icon-font/
        expandTooltip: "View Legend", // optional, defaults to "Expand" for English locale
        group: "bottom-right",
        content: 
          new Legend({ 
            view: this.view,
            layerInfos: [ 
               { layer: guns, title: "Gun Legend" },
               { layer: domains, title: "Domain Legend" },
               { layer: kunis, title: "Kuni Legend" }]
          }), 
      });

      /*******************************************  
                Export (Bottom Right)
      ********************************************/

      // EXPORT WIDGET
      // let printTemplate = new printTemplate({
      //   layoutOptions: {
      //     titleText: "My Print",
      //     authorText: "Sam",
      //     copyrightText: "My Company",
      //     scalebarUnit: "Miles",
      //     // the following text elements must
      //     // exist in the print service to appear
      //     customTextElements: [
      //       {"description": "My description"},
      //       {"location": "My Location"},
      //       {"date": "11/11/2020, 11:11:20 AM"}
      //     ]
      //   }
      // });

      let exportExpand = new Expand({
        view: this.view,
        expandIconClass: "esri-icon-printer",  // see https://developers.arcgis.com/javascript/latest/guide/esri-icon-font/
        expandTooltip: "Export Map", // optional, defaults to "Expand" for English locale
        group: "bottom-right",
        content: new Print({
          view: this.view,
          templateOptions: new TemplateOptions({
            title: "My Print",
            author: "Sam",
            copyright: "My Company",
            legendEnabled: true
            // the following text elements must
            // exist in the print service to appear
            // customTextElements: [
            //   {"description": "My description"},
            //   {"location": "My Location"},
            //   {"date": "11/11/2020, 11:11:20 AM"}
            // ]
          }),
          printServiceUrl:
                "https://utility.arcgisonline.com/arcgis/rest/services/Utilities/PrintingTools/GPServer/Export%20Web%20Map%20Task"
          })
      });

      // Add bottom right widgets to UI
      // this.legends = legendExpand

      /*******************************************  
                Search (Top Right)
      ********************************************/

      // Generate the sources for search based on hardcoded layer info under mounted()
      let searchSources = []
      Object.values(this.layerInfo).forEach((layerData) => {
        let source = {
          layer: this.layers[layerData.layer_name.toLowerCase()],
          searchFields: layerData.fields.map(field => {
            if (field.search)
              return field.id;
          }).filter(id => id != null),
          displayField: layerData.fields[0].id,
          // TODO : Add a generator function for suggestions based on layer info
          // suggestionTemplate: "name: {fukuivil_2}<br> {fukuivil_3}-{fukuivil_4}",
          exactMatch: false,
          outFields: ["*"],
          name: layerData.layer_name,
          placeholder: `Search for ${layerData.layer_name}`,
          zoomScale: layerData.zoom_scale,
          maxSuggestions: 20,
          maxResults: 20,
        };

        searchSources.push(source);
      })

      // Setting sources property of the search widget to use two layer sources.
      var searchWidget = new Search({
        view: this.view,
        allPlaceholder: "Search Gun / Village / Kuni",
        includeDefaultSources: false,
        group: "top-right",
        sources: searchSources,
        // autoSelect: false,
        // suggestionsEnabled: false,
      });

      searchWidget.on("suggest-complete", function () {
        if (searchWidget.suggestions != null) {
          searchWidget.suggestions[0].results.sort(suggestionsCompare);
        }
      });

      function suggestionsCompare(a, b) {
        if (a.text.length < b.text.length)
          return -1;
        if (a.text.length > b.text.length)
          return 1;
        return 0; // equal
      }

      /*******************************************  
                Base Map (Top Right)
      ********************************************/

      // Create other Expandable widgets
      let basemapExpand = new Expand({
        view: this.view,
        expandIconClass: "esri-icon-basemap",
        expandTooltip: "Select a Basemap",
        group: "top-right",
        content: new BasemapGallery({
          view: this.view,
          source: {
            portal: {
              url: "https://www.arcgis.com",
              useVectorBasemaps: true  // Load vector tile basemaps
            }}}),
      });

      /*******************************************  
                Layer List (Top Right)
      ********************************************/

      let layerListExpand = new Expand({
        view: this.view,
        expandIconClass: "esri-icon-layers",  // see https://developers.arcgis.com/javascript/latest/guide/esri-icon-font/
        expandTooltip: "Expand LayerList", // optional, defaults to "Expand" for English locale
        group: "top-right",
        content: new LayerList({
          container: document.createElement("div"),
          view: this.view
        }),
      });

      /*******************************************  
                Add the widgets
      ********************************************/
      this.view.ui.add([this.legendExpand, exportExpand], "bottom-right");
      this.view.ui.add([searchWidget, layerListExpand, basemapExpand], "top-right");
      

      /* =====================================   EXPORT BETA CODE    ============================================= */

      var data = new URLSearchParams();
      data.append('Web_Map_as_JSON', JSON.stringify({"operationalLayers":[{"type":"VectorTileLayer","styleUrl":"https://www.arcgis.com/sharing/rest/content/items/8a2cba3b0ebf4140b7c0dc5ee149549a/resources/styles/root.json","id":"gray-base-layer","title":"World Light Gray","opacity":1,"minScale":0,"maxScale":0},{"url":"https://services1.arcgis.com/7uJv7I3kgh2y7Pe0/arcgis/rest/services/Files_v4/FeatureServer/3","id":"1706e5bdfb5-layer-5","title":"Files v4 - Gun","showLabels":true,"opacity":1,"minScale":0,"maxScale":0},{"url":"https://services1.arcgis.com/7uJv7I3kgh2y7Pe0/arcgis/rest/services/Files_v4/FeatureServer/4","id":"1706e5bdfb5-layer-6","opacity":0.8,"title":"Files v4 - Villages to domains","showLabels":true,"minScale":0,"maxScale":0},{"url":"https://services1.arcgis.com/7uJv7I3kgh2y7Pe0/arcgis/rest/services/overlays/FeatureServer/1","id":"1706e5bdfb5-layer-8","title":"Overlays - Uncertainbelonging","showLabels":true,"opacity":1,"minScale":0,"maxScale":0},{"url":"https://services1.arcgis.com/7uJv7I3kgh2y7Pe0/arcgis/rest/services/overlays/FeatureServer/0","id":"1706e5bdfb5-layer-9","title":"Overlays - Boundarychanges","layerDefinition":{"drawingInfo":{"renderer":{"type":"uniqueValue","field1":"changefr_2","field2":"changetoDo","legendOptions":{"title":"Uncertanties:"},"defaultLabel":"DEFAULT LABEL","defaultSymbol":{"type":"esriSFS","color":[26,26,26,255],"outline":{"type":"esriSLS","color":[0,0,0,255],"width":0.75,"style":"esriSLSSolid"},"style":"esriSFSSolid"},"fieldDelimiter":", ","uniqueValueInfos":[{"label":"Fukui to Oono","symbol":{"type":"esriPFS","color":[0,0,0,255],"url":"http://localhost:3000/red_yellow.jpg","xscale":1,"yscale":1,"width":500,"height":500,"xoffset":0,"yoffset":0},"value":"Fukui, Oono"},{"label":"Sabae to Fukui","symbol":{"type":"esriPFS","color":[0,0,0,255],"url":"http://localhost:3000/red_green.jpg","xscale":1,"yscale":1,"width":500,"height":500,"xoffset":0,"yoffset":0},"value":"Sabae, Fukui"}]}}},"showLabels":true,"opacity":1,"minScale":0,"maxScale":0}],"mapOptions":{"extent":{"spatialReference":{"latestWkid":3857,"wkid":102100},"xmin":14975258.010328524,"ymin":4223777.491982939,"xmax":15205181.051256388,"ymax":4429546.383664394},"spatialReference":{"latestWkid":3857,"wkid":102100},"showAttribution":true,"scale":1155583.4197442674,"time": [-8488800000000]},"exportOptions":{"dpi":96},"layoutOptions":{"titleText":"My Print","authorText":"Sam","copyrightText":"My Company","scaleBarOptions":{},"legendOptions":{"operationalLayers":[{"id":"1706e5bdfb5-layer-5"},{"id":"1706e5bdfb5-layer-6"},{"id":"1706e5bdfb5-layer-8"},{"id":"1706e5bdfb5-layer-9"}]}}}))
      data.append('Format', 'PDF')
      data.append('Layout_Template', 'Letter ANSI A Landscape')
      data.append('returnFeatureCollection', 'false')
      data.append('returnM', 'false')
      data.append('returnZ', 'false')
      data.append('f', 'json')

      var url = "https://utility.arcgisonline.com/arcgis/rest/services/Utilities/PrintingTools/GPServer/Export%20Web%20Map%20Task/execute"
      // formData = JSON.stringify({"Web_Map_as_JSON":{"operationalLayers":[{"type":"VectorTileLayer","styleUrl":"https://www.arcgis.com/sharing/rest/content/items/8a2cba3b0ebf4140b7c0dc5ee149549a/resources/styles/root.json","id":"gray-base-layer","title":"World Light Gray","opacity":1,"minScale":0,"maxScale":0},{"url":"https://services1.arcgis.com/7uJv7I3kgh2y7Pe0/arcgis/rest/services/Files_v4/FeatureServer/3","id":"1706e5bdfb5-layer-5","title":"Files v4 - Gun","showLabels":true,"opacity":1,"minScale":0,"maxScale":0},{"url":"https://services1.arcgis.com/7uJv7I3kgh2y7Pe0/arcgis/rest/services/Files_v4/FeatureServer/4","id":"1706e5bdfb5-layer-6","opacity":0.8,"title":"Files v4 - Villages to domains","showLabels":true,"minScale":0,"maxScale":0},{"url":"https://services1.arcgis.com/7uJv7I3kgh2y7Pe0/arcgis/rest/services/overlays/FeatureServer/1","id":"1706e5bdfb5-layer-8","title":"Overlays - Uncertainbelonging","showLabels":true,"opacity":1,"minScale":0,"maxScale":0},{"url":"https://services1.arcgis.com/7uJv7I3kgh2y7Pe0/arcgis/rest/services/overlays/FeatureServer/0","id":"1706e5bdfb5-layer-9","title":"Overlays - Boundarychanges","layerDefinition":{"drawingInfo":{"renderer":{"type":"uniqueValue","field1":"changefr_2","field2":"changetoDo","legendOptions":{"title":"Uncertanties:"},"defaultLabel":"DEFAULT LABEL","defaultSymbol":{"type":"esriSFS","color":[26,26,26,255],"outline":{"type":"esriSLS","color":[0,0,0,255],"width":0.75,"style":"esriSLSSolid"},"style":"esriSFSSolid"},"fieldDelimiter":", ","uniqueValueInfos":[{"label":"Fukui to Oono","symbol":{"type":"esriPFS","color":[0,0,0,255],"url":"http://localhost:3000/red_yellow.jpg","xscale":1,"yscale":1,"width":500,"height":500,"xoffset":0,"yoffset":0},"value":"Fukui, Oono"},{"label":"Sabae to Fukui","symbol":{"type":"esriPFS","color":[0,0,0,255],"url":"http://localhost:3000/red_green.jpg","xscale":1,"yscale":1,"width":500,"height":500,"xoffset":0,"yoffset":0},"value":"Sabae, Fukui"}]}}},"showLabels":true,"opacity":1,"minScale":0,"maxScale":0}],"mapOptions":{"extent":{"spatialReference":{"latestWkid":3857,"wkid":102100},"xmin":14975258.010328524,"ymin":4223777.491982939,"xmax":15205181.051256388,"ymax":4429546.383664394},"spatialReference":{"latestWkid":3857,"wkid":102100},"showAttribution":true,"scale":1155583.4197442674},"exportOptions":{"dpi":96},"layoutOptions":{"titleText":"My Print","authorText":"Sam","copyrightText":"My Company","scaleBarOptions":{},"legendOptions":{"operationalLayers":[{"id":"1706e5bdfb5-layer-5"},{"id":"1706e5bdfb5-layer-6"},{"id":"1706e5bdfb5-layer-8"},{"id":"1706e5bdfb5-layer-9"}]}}}})
      
      fetch(url, {
        method: 'POST',
        body: data,
      })
      .then((response) => {
        return response.json();
      })
      .then((myJson) => {
        console.log(myJson);
        console.log(myJson.results[0].value.url);
      })
      .catch((error) => {
        console.error('Error:', error);
      });

    
    /* =====================================   LAYER WATCHES    ============================================= */

    // Skeleton watching for updates to the view extent, will be used laer
    watchUtils.whenTrue(this.view, "stationary", () => {
      // Get the extent of the view once it has stopped being moved by useVectorBasemaps
      if (this.view.extent) {
        var info =
          "<br> <span> the view extent changed: </span>" +
          "<br> xmin:" + this.view.extent.xmin.toFixed(2) +
          " xmax: " + this.view.extent.xmax.toFixed(2) +
          "<br> ymin:" + this.view.extent.ymin.toFixed(2) +
          " ymax: " + this.view.extent.ymax.toFixed(2);
          console.log(info);
      }
    });

    // Code for the loading screen at beginning
    setTimeout(() => {
      console.log("LOADING COMPLETE TIMER")
      this.isLoading = false
    }, 12000)

    this.isMounted = true;
    /* =====================================   END OF MAP CDOE    ============================================= */
    });
  },
  beforeDestroy() {
    if (this.view) {
      // destroy the map view
      this.view.container = null;
    }
  }
};

</script>

<style scoped>
#map {
  padding: 0;
  margin: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}
#viewDiv {
  padding: 0;
  margin: 0;
  width: 100%;
  height: 100%;
}

#timeSlider {
  position: absolute;
  left: 100px;
  right: 100px;
  bottom: 30px;
}
</style>
