# Extjs

## Tree Grid\(3.4\)

### Resize

```text
    window.treeObj.onResize(x, y);
    window.treeObj.columns[i].width = x;
    window.treeObj.updateColumnWidths();
```

### Reload Data

```text
    window.treeObj.getLoader().dataUrl = url;
    window.treeObj.getRootNode().reload();
```

### Select Leaf

```text
    window.treeObj.selectPath(node.id);
```

## Tree\(4.0+\)

### Init

```text
    Ext.onReady(function() {
        var treeStore = Ext.create('Ext.data.TreeStore', {
            proxy: {
                type: 'ajax',
                url: '/extjs/treeData'
            },
            fields: ['text', 'leaf', 'cataId']
        });

        var CatalogTtree = Ext.create('Ext.tree.Panel', {
            store: treeStore,
            border: true,  
            renderTo: 'treeDiv',
            enableDD: true,
            width:400,
            root: {
              'text': 'Casa',
              'cataId': '1',
              'expanded': true
            },
            rootVisible: true,  
            useArrows:true,
            containerScroll: true,
            collapsible: false,
            autoScroll: false,
            tbar: [
              {
                 'text': 'Debug',
                 handler: function(){
                    alert(1);
                 }
              }, '-', {
                 'text': 'haha',
                 handler: function(){
                    alert(2);
                 }
              }
            ],
            listeners: {
              'itemcontextmenu': function(view,record,item,index,e,eOpts){
                 e.preventDefault();
                 e.stopEvent();
                 var menu = new Ext.menu.Menu({
                    float:true,
                    items:[{
                       text:"修改",
                       iconCls:'leaf',
                       handler:function(){
                          this.up("menu").hide();
                          window.extWin.show();
                       }
                    }]
                 }).showAt(e.getXY());
              }
            }              
        });

        window.extWin = new Ext.Window({
           title:'Add Folder/Chapter',
           layout:'form',
           width:250,
           closeAction:'close',
           target : document.getElementById('buttonId'),
           plain: true,
           items: [{
              xtype : 'textfield',
              fieldLabel: 'Name'
           }],
           buttons: [{
              text: 'Cancel',
              handler: function(){window.extWin.close();}
           }, {
              text: 'Submit',
              handler: function(){Ext.Msg.alert('Message Sent', 'Your msg is sent');}
           }],
           buttonAlign: 'center',
        });
     });
```

