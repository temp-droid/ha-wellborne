var Ee=Object.defineProperty;var ft=Object.getOwnPropertyDescriptor;var m=(n,e)=>()=>(n&&(e=n(n=0)),e);var mt=(n,e)=>{for(var t in e)Ee(n,t,{get:e[t],enumerable:!0})};var S=(n,e,t,r)=>{for(var i=r>1?void 0:r?ft(e,t):e,s=n.length-1,o;s>=0;s--)(o=n[s])&&(i=(r?o(e,t,i):o(i))||i);return r&&i&&Ee(e,t,i),i};var J,Q,ae,Se,I,Ce,D,Re,ce,le=m(()=>{J=globalThis,Q=J.ShadowRoot&&(J.ShadyCSS===void 0||J.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,ae=Symbol(),Se=new WeakMap,I=class{constructor(e,t,r){if(this._$cssResult$=!0,r!==ae)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=e,this.t=t}get styleSheet(){let e=this.o,t=this.t;if(Q&&e===void 0){let r=t!==void 0&&t.length===1;r&&(e=Se.get(t)),e===void 0&&((this.o=e=new CSSStyleSheet).replaceSync(this.cssText),r&&Se.set(t,e))}return e}toString(){return this.cssText}},Ce=n=>new I(typeof n=="string"?n:n+"",void 0,ae),D=(n,...e)=>{let t=n.length===1?n[0]:e.reduce((r,i,s)=>r+(o=>{if(o._$cssResult$===!0)return o.cssText;if(typeof o=="number")return o;throw Error("Value passed to 'css' function must be a 'css' function result: "+o+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(i)+n[s+1],n[0]);return new I(t,n,ae)},Re=(n,e)=>{if(Q)n.adoptedStyleSheets=e.map(t=>t instanceof CSSStyleSheet?t:t.styleSheet);else for(let t of e){let r=document.createElement("style"),i=J.litNonce;i!==void 0&&r.setAttribute("nonce",i),r.textContent=t.cssText,n.appendChild(r)}},ce=Q?n=>n:n=>n instanceof CSSStyleSheet?(e=>{let t="";for(let r of e.cssRules)t+=r.cssText;return Ce(t)})(n):n});var gt,_t,yt,vt,bt,$t,X,ke,xt,wt,z,W,ee,Te,b,j=m(()=>{le();le();({is:gt,defineProperty:_t,getOwnPropertyDescriptor:yt,getOwnPropertyNames:vt,getOwnPropertySymbols:bt,getPrototypeOf:$t}=Object),X=globalThis,ke=X.trustedTypes,xt=ke?ke.emptyScript:"",wt=X.reactiveElementPolyfillSupport,z=(n,e)=>n,W={toAttribute(n,e){switch(e){case Boolean:n=n?xt:null;break;case Object:case Array:n=n==null?n:JSON.stringify(n)}return n},fromAttribute(n,e){let t=n;switch(e){case Boolean:t=n!==null;break;case Number:t=n===null?null:Number(n);break;case Object:case Array:try{t=JSON.parse(n)}catch{t=null}}return t}},ee=(n,e)=>!gt(n,e),Te={attribute:!0,type:String,converter:W,reflect:!1,useDefault:!1,hasChanged:ee};Symbol.metadata??=Symbol("metadata"),X.litPropertyMetadata??=new WeakMap;b=class extends HTMLElement{static addInitializer(e){this._$Ei(),(this.l??=[]).push(e)}static get observedAttributes(){return this.finalize(),this._$Eh&&[...this._$Eh.keys()]}static createProperty(e,t=Te){if(t.state&&(t.attribute=!1),this._$Ei(),this.prototype.hasOwnProperty(e)&&((t=Object.create(t)).wrapped=!0),this.elementProperties.set(e,t),!t.noAccessor){let r=Symbol(),i=this.getPropertyDescriptor(e,r,t);i!==void 0&&_t(this.prototype,e,i)}}static getPropertyDescriptor(e,t,r){let{get:i,set:s}=yt(this.prototype,e)??{get(){return this[t]},set(o){this[t]=o}};return{get:i,set(o){let a=i?.call(this);s?.call(this,o),this.requestUpdate(e,a,r)},configurable:!0,enumerable:!0}}static getPropertyOptions(e){return this.elementProperties.get(e)??Te}static _$Ei(){if(this.hasOwnProperty(z("elementProperties")))return;let e=$t(this);e.finalize(),e.l!==void 0&&(this.l=[...e.l]),this.elementProperties=new Map(e.elementProperties)}static finalize(){if(this.hasOwnProperty(z("finalized")))return;if(this.finalized=!0,this._$Ei(),this.hasOwnProperty(z("properties"))){let t=this.properties,r=[...vt(t),...bt(t)];for(let i of r)this.createProperty(i,t[i])}let e=this[Symbol.metadata];if(e!==null){let t=litPropertyMetadata.get(e);if(t!==void 0)for(let[r,i]of t)this.elementProperties.set(r,i)}this._$Eh=new Map;for(let[t,r]of this.elementProperties){let i=this._$Eu(t,r);i!==void 0&&this._$Eh.set(i,t)}this.elementStyles=this.finalizeStyles(this.styles)}static finalizeStyles(e){let t=[];if(Array.isArray(e)){let r=new Set(e.flat(1/0).reverse());for(let i of r)t.unshift(ce(i))}else e!==void 0&&t.push(ce(e));return t}static _$Eu(e,t){let r=t.attribute;return r===!1?void 0:typeof r=="string"?r:typeof e=="string"?e.toLowerCase():void 0}constructor(){super(),this._$Ep=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Em=null,this._$Ev()}_$Ev(){this._$ES=new Promise(e=>this.enableUpdating=e),this._$AL=new Map,this._$E_(),this.requestUpdate(),this.constructor.l?.forEach(e=>e(this))}addController(e){(this._$EO??=new Set).add(e),this.renderRoot!==void 0&&this.isConnected&&e.hostConnected?.()}removeController(e){this._$EO?.delete(e)}_$E_(){let e=new Map,t=this.constructor.elementProperties;for(let r of t.keys())this.hasOwnProperty(r)&&(e.set(r,this[r]),delete this[r]);e.size>0&&(this._$Ep=e)}createRenderRoot(){let e=this.shadowRoot??this.attachShadow(this.constructor.shadowRootOptions);return Re(e,this.constructor.elementStyles),e}connectedCallback(){this.renderRoot??=this.createRenderRoot(),this.enableUpdating(!0),this._$EO?.forEach(e=>e.hostConnected?.())}enableUpdating(e){}disconnectedCallback(){this._$EO?.forEach(e=>e.hostDisconnected?.())}attributeChangedCallback(e,t,r){this._$AK(e,r)}_$ET(e,t){let r=this.constructor.elementProperties.get(e),i=this.constructor._$Eu(e,r);if(i!==void 0&&r.reflect===!0){let s=(r.converter?.toAttribute!==void 0?r.converter:W).toAttribute(t,r.type);this._$Em=e,s==null?this.removeAttribute(i):this.setAttribute(i,s),this._$Em=null}}_$AK(e,t){let r=this.constructor,i=r._$Eh.get(e);if(i!==void 0&&this._$Em!==i){let s=r.getPropertyOptions(i),o=typeof s.converter=="function"?{fromAttribute:s.converter}:s.converter?.fromAttribute!==void 0?s.converter:W;this._$Em=i;let a=o.fromAttribute(t,s.type);this[i]=a??this._$Ej?.get(i)??a,this._$Em=null}}requestUpdate(e,t,r,i=!1,s){if(e!==void 0){let o=this.constructor;if(i===!1&&(s=this[e]),r??=o.getPropertyOptions(e),!((r.hasChanged??ee)(s,t)||r.useDefault&&r.reflect&&s===this._$Ej?.get(e)&&!this.hasAttribute(o._$Eu(e,r))))return;this.C(e,t,r)}this.isUpdatePending===!1&&(this._$ES=this._$EP())}C(e,t,{useDefault:r,reflect:i,wrapped:s},o){r&&!(this._$Ej??=new Map).has(e)&&(this._$Ej.set(e,o??t??this[e]),s!==!0||o!==void 0)||(this._$AL.has(e)||(this.hasUpdated||r||(t=void 0),this._$AL.set(e,t)),i===!0&&this._$Em!==e&&(this._$Eq??=new Set).add(e))}async _$EP(){this.isUpdatePending=!0;try{await this._$ES}catch(t){Promise.reject(t)}let e=this.scheduleUpdate();return e!=null&&await e,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){if(!this.isUpdatePending)return;if(!this.hasUpdated){if(this.renderRoot??=this.createRenderRoot(),this._$Ep){for(let[i,s]of this._$Ep)this[i]=s;this._$Ep=void 0}let r=this.constructor.elementProperties;if(r.size>0)for(let[i,s]of r){let{wrapped:o}=s,a=this[i];o!==!0||this._$AL.has(i)||a===void 0||this.C(i,void 0,s,a)}}let e=!1,t=this._$AL;try{e=this.shouldUpdate(t),e?(this.willUpdate(t),this._$EO?.forEach(r=>r.hostUpdate?.()),this.update(t)):this._$EM()}catch(r){throw e=!1,this._$EM(),r}e&&this._$AE(t)}willUpdate(e){}_$AE(e){this._$EO?.forEach(t=>t.hostUpdated?.()),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(e)),this.updated(e)}_$EM(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$ES}shouldUpdate(e){return!0}update(e){this._$Eq&&=this._$Eq.forEach(t=>this._$ET(t,this[t])),this._$EM()}updated(e){}firstUpdated(e){}};b.elementStyles=[],b.shadowRootOptions={mode:"open"},b[z("elementProperties")]=new Map,b[z("finalized")]=new Map,wt?.({ReactiveElement:b}),(X.reactiveElementVersions??=[]).push("2.1.2")});function We(n,e){if(!_e(n)||!n.hasOwnProperty("raw"))throw Error("invalid template strings array");return He!==void 0?He.createHTML(e):e}function M(n,e,t=n,r){if(e===T)return e;let i=r!==void 0?t._$Co?.[r]:t._$Cl,s=B(e)?void 0:e._$litDirective$;return i?.constructor!==s&&(i?._$AO?.(!1),s===void 0?i=void 0:(i=new s(n),i._$AT(n,t,r)),r!==void 0?(t._$Co??=[])[r]=i:t._$Cl=i),i!==void 0&&(e=M(n,i._$AS(n,e.values),i,r)),e}var ge,Pe,te,He,Ie,w,De,At,k,K,B,_e,Et,pe,F,Me,Ne,C,Le,Oe,ze,ye,f,A,qt,T,l,Ue,R,St,q,he,G,N,de,ue,fe,me,Ct,je,re=m(()=>{ge=globalThis,Pe=n=>n,te=ge.trustedTypes,He=te?te.createPolicy("lit-html",{createHTML:n=>n}):void 0,Ie="$lit$",w=`lit$${Math.random().toFixed(9).slice(2)}$`,De="?"+w,At=`<${De}>`,k=document,K=()=>k.createComment(""),B=n=>n===null||typeof n!="object"&&typeof n!="function",_e=Array.isArray,Et=n=>_e(n)||typeof n?.[Symbol.iterator]=="function",pe=`[ 	
\f\r]`,F=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,Me=/-->/g,Ne=/>/g,C=RegExp(`>|${pe}(?:([^\\s"'>=/]+)(${pe}*=${pe}*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`,"g"),Le=/'/g,Oe=/"/g,ze=/^(?:script|style|textarea|title)$/i,ye=n=>(e,...t)=>({_$litType$:n,strings:e,values:t}),f=ye(1),A=ye(2),qt=ye(3),T=Symbol.for("lit-noChange"),l=Symbol.for("lit-nothing"),Ue=new WeakMap,R=k.createTreeWalker(k,129);St=(n,e)=>{let t=n.length-1,r=[],i,s=e===2?"<svg>":e===3?"<math>":"",o=F;for(let a=0;a<t;a++){let c=n[a],p,d,h=-1,_=0;for(;_<c.length&&(o.lastIndex=_,d=o.exec(c),d!==null);)_=o.lastIndex,o===F?d[1]==="!--"?o=Me:d[1]!==void 0?o=Ne:d[2]!==void 0?(ze.test(d[2])&&(i=RegExp("</"+d[2],"g")),o=C):d[3]!==void 0&&(o=C):o===C?d[0]===">"?(o=i??F,h=-1):d[1]===void 0?h=-2:(h=o.lastIndex-d[2].length,p=d[1],o=d[3]===void 0?C:d[3]==='"'?Oe:Le):o===Oe||o===Le?o=C:o===Me||o===Ne?o=F:(o=C,i=void 0);let g=o===C&&n[a+1].startsWith("/>")?" ":"";s+=o===F?c+At:h>=0?(r.push(p),c.slice(0,h)+Ie+c.slice(h)+w+g):c+w+(h===-2?a:g)}return[We(n,s+(n[t]||"<?>")+(e===2?"</svg>":e===3?"</math>":"")),r]},q=class n{constructor({strings:e,_$litType$:t},r){let i;this.parts=[];let s=0,o=0,a=e.length-1,c=this.parts,[p,d]=St(e,t);if(this.el=n.createElement(p,r),R.currentNode=this.el.content,t===2||t===3){let h=this.el.content.firstChild;h.replaceWith(...h.childNodes)}for(;(i=R.nextNode())!==null&&c.length<a;){if(i.nodeType===1){if(i.hasAttributes())for(let h of i.getAttributeNames())if(h.endsWith(Ie)){let _=d[o++],g=i.getAttribute(h).split(w),x=/([.?@])?(.*)/.exec(_);c.push({type:1,index:s,name:x[2],strings:g,ctor:x[1]==="."?de:x[1]==="?"?ue:x[1]==="@"?fe:N}),i.removeAttribute(h)}else h.startsWith(w)&&(c.push({type:6,index:s}),i.removeAttribute(h));if(ze.test(i.tagName)){let h=i.textContent.split(w),_=h.length-1;if(_>0){i.textContent=te?te.emptyScript:"";for(let g=0;g<_;g++)i.append(h[g],K()),R.nextNode(),c.push({type:2,index:++s});i.append(h[_],K())}}}else if(i.nodeType===8)if(i.data===De)c.push({type:2,index:s});else{let h=-1;for(;(h=i.data.indexOf(w,h+1))!==-1;)c.push({type:7,index:s}),h+=w.length-1}s++}}static createElement(e,t){let r=k.createElement("template");return r.innerHTML=e,r}};he=class{constructor(e,t){this._$AV=[],this._$AN=void 0,this._$AD=e,this._$AM=t}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(e){let{el:{content:t},parts:r}=this._$AD,i=(e?.creationScope??k).importNode(t,!0);R.currentNode=i;let s=R.nextNode(),o=0,a=0,c=r[0];for(;c!==void 0;){if(o===c.index){let p;c.type===2?p=new G(s,s.nextSibling,this,e):c.type===1?p=new c.ctor(s,c.name,c.strings,this,e):c.type===6&&(p=new me(s,this,e)),this._$AV.push(p),c=r[++a]}o!==c?.index&&(s=R.nextNode(),o++)}return R.currentNode=k,i}p(e){let t=0;for(let r of this._$AV)r!==void 0&&(r.strings!==void 0?(r._$AI(e,r,t),t+=r.strings.length-2):r._$AI(e[t])),t++}},G=class n{get _$AU(){return this._$AM?._$AU??this._$Cv}constructor(e,t,r,i){this.type=2,this._$AH=l,this._$AN=void 0,this._$AA=e,this._$AB=t,this._$AM=r,this.options=i,this._$Cv=i?.isConnected??!0}get parentNode(){let e=this._$AA.parentNode,t=this._$AM;return t!==void 0&&e?.nodeType===11&&(e=t.parentNode),e}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(e,t=this){e=M(this,e,t),B(e)?e===l||e==null||e===""?(this._$AH!==l&&this._$AR(),this._$AH=l):e!==this._$AH&&e!==T&&this._(e):e._$litType$!==void 0?this.$(e):e.nodeType!==void 0?this.T(e):Et(e)?this.k(e):this._(e)}O(e){return this._$AA.parentNode.insertBefore(e,this._$AB)}T(e){this._$AH!==e&&(this._$AR(),this._$AH=this.O(e))}_(e){this._$AH!==l&&B(this._$AH)?this._$AA.nextSibling.data=e:this.T(k.createTextNode(e)),this._$AH=e}$(e){let{values:t,_$litType$:r}=e,i=typeof r=="number"?this._$AC(e):(r.el===void 0&&(r.el=q.createElement(We(r.h,r.h[0]),this.options)),r);if(this._$AH?._$AD===i)this._$AH.p(t);else{let s=new he(i,this),o=s.u(this.options);s.p(t),this.T(o),this._$AH=s}}_$AC(e){let t=Ue.get(e.strings);return t===void 0&&Ue.set(e.strings,t=new q(e)),t}k(e){_e(this._$AH)||(this._$AH=[],this._$AR());let t=this._$AH,r,i=0;for(let s of e)i===t.length?t.push(r=new n(this.O(K()),this.O(K()),this,this.options)):r=t[i],r._$AI(s),i++;i<t.length&&(this._$AR(r&&r._$AB.nextSibling,i),t.length=i)}_$AR(e=this._$AA.nextSibling,t){for(this._$AP?.(!1,!0,t);e!==this._$AB;){let r=Pe(e).nextSibling;Pe(e).remove(),e=r}}setConnected(e){this._$AM===void 0&&(this._$Cv=e,this._$AP?.(e))}},N=class{get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}constructor(e,t,r,i,s){this.type=1,this._$AH=l,this._$AN=void 0,this.element=e,this.name=t,this._$AM=i,this.options=s,r.length>2||r[0]!==""||r[1]!==""?(this._$AH=Array(r.length-1).fill(new String),this.strings=r):this._$AH=l}_$AI(e,t=this,r,i){let s=this.strings,o=!1;if(s===void 0)e=M(this,e,t,0),o=!B(e)||e!==this._$AH&&e!==T,o&&(this._$AH=e);else{let a=e,c,p;for(e=s[0],c=0;c<s.length-1;c++)p=M(this,a[r+c],t,c),p===T&&(p=this._$AH[c]),o||=!B(p)||p!==this._$AH[c],p===l?e=l:e!==l&&(e+=(p??"")+s[c+1]),this._$AH[c]=p}o&&!i&&this.j(e)}j(e){e===l?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,e??"")}},de=class extends N{constructor(){super(...arguments),this.type=3}j(e){this.element[this.name]=e===l?void 0:e}},ue=class extends N{constructor(){super(...arguments),this.type=4}j(e){this.element.toggleAttribute(this.name,!!e&&e!==l)}},fe=class extends N{constructor(e,t,r,i,s){super(e,t,r,i,s),this.type=5}_$AI(e,t=this){if((e=M(this,e,t,0)??l)===T)return;let r=this._$AH,i=e===l&&r!==l||e.capture!==r.capture||e.once!==r.once||e.passive!==r.passive,s=e!==l&&(r===l||i);i&&this.element.removeEventListener(this.name,this,r),s&&this.element.addEventListener(this.name,this,e),this._$AH=e}handleEvent(e){typeof this._$AH=="function"?this._$AH.call(this.options?.host??this.element,e):this._$AH.handleEvent(e)}},me=class{constructor(e,t,r){this.element=e,this.type=6,this._$AN=void 0,this._$AM=t,this.options=r}get _$AU(){return this._$AM._$AU}_$AI(e){M(this,e)}},Ct=ge.litHtmlPolyfillSupport;Ct?.(q,G),(ge.litHtmlVersions??=[]).push("3.3.3");je=(n,e,t)=>{let r=t?.renderBefore??e,i=r._$litPart$;if(i===void 0){let s=t?.renderBefore??null;r._$litPart$=i=new G(e.insertBefore(K(),s),s,void 0,t??{})}return i._$AI(n),i}});var ve,v,Rt,Fe=m(()=>{j();j();re();re();ve=globalThis,v=class extends b{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){let e=super.createRenderRoot();return this.renderOptions.renderBefore??=e.firstChild,e}update(e){let t=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(e),this._$Do=je(t,this.renderRoot,this.renderOptions)}connectedCallback(){super.connectedCallback(),this._$Do?.setConnected(!0)}disconnectedCallback(){super.disconnectedCallback(),this._$Do?.setConnected(!1)}render(){return T}};v._$litElement$=!0,v.finalized=!0,ve.litElementHydrateSupport?.({LitElement:v});Rt=ve.litElementPolyfillSupport;Rt?.({LitElement:v});(ve.litElementVersions??=[]).push("4.2.2")});var Ke=m(()=>{});var L=m(()=>{j();re();Fe();Ke()});var Be=m(()=>{});function ie(n){return(e,t)=>typeof t=="object"?Tt(n,e,t):((r,i,s)=>{let o=i.hasOwnProperty(s);return i.constructor.createProperty(s,r),o?Object.getOwnPropertyDescriptor(i,s):void 0})(n,e,t)}var kt,Tt,be=m(()=>{j();kt={attribute:!0,type:String,converter:W,reflect:!1,hasChanged:ee},Tt=(n=kt,e,t)=>{let{kind:r,metadata:i}=t,s=globalThis.litPropertyMetadata.get(i);if(s===void 0&&globalThis.litPropertyMetadata.set(i,s=new Map),r==="setter"&&((n=Object.create(n)).wrapped=!0),s.set(t.name,n),r==="accessor"){let{name:o}=t;return{set(a){let c=e.get.call(this);e.set.call(this,a),this.requestUpdate(o,c,n,!0,a)},init(a){return a!==void 0&&this.C(o,void 0,n,a),a}}}if(r==="setter"){let{name:o}=t;return function(a){let c=this[o];e.call(this,a),this.requestUpdate(o,c,n,!0,a)}}throw Error("Unsupported decorator location: "+r)}});function O(n){return ie({...n,state:!0,attribute:!1})}var qe=m(()=>{be();});var Ge=m(()=>{});var U=m(()=>{});var Ve=m(()=>{U();});var Ye=m(()=>{U();});var Ze=m(()=>{U();});var Je=m(()=>{U();});var Qe=m(()=>{U();});var $e=m(()=>{Be();be();qe();Ge();Ve();Ye();Ze();Je();Qe()});var V,Y,et,se,oe,tt,$,y,xe,Z=m(()=>{"use strict";V="wellborne-charger-card",Y="wellborne-charger-card-editor",et="1.0.0",se="wellborne",oe={power:"power",energy:"energy",current:"current",session_duration:"session_duration",status:"status",added_range:"added_range",monthly_energy:"monthly_energy",yearly_energy:"yearly_energy",last_session_energy:"last_session_energy",last_session_duration:"last_session_duration",wifi_ssid:"wifi_ssid",charging:"charging",charger_online:"charger_online",vehicle_connected:"vehicle_connected"},tt=new Set(["charging","charger_online","vehicle_connected"]),$=new Set(["unavailable","unknown","none",""]),y="\u2014",xe={show_curve:!0,show_totals:!0,show_cost:!0,curve_hours:4}});var lt={};mt(lt,{WellborneChargerCardEditor:()=>P});var It,P,we=m(()=>{"use strict";L();$e();Z();It=[{key:"show_curve",label:"Power curve (sparkline)"},{key:"show_totals",label:"Month / year totals"},{key:"show_cost",label:"Last-charge cost"}],P=class extends v{setConfig(e){this._config=e}render(){if(!this._config)return l;let e=this._config;return f`
      <div class="form">
        ${this._renderDevicePicker(e)}

        <label class="field">
          <span>Name (optional)</span>
          <input
            type="text"
            .value=${e.name??""}
            @input=${t=>this._set("name",t.target.value||void 0)}
          />
        </label>

        <label class="field">
          <span>Battery entity (car SoC, optional)</span>
          <input
            type="text"
            placeholder="sensor.ioniq5_battery_level"
            .value=${e.battery_entity??""}
            @input=${t=>this._set("battery_entity",t.target.value||void 0)}
          />
        </label>

        <label class="field">
          <span>Price entity (€/kWh, optional)</span>
          <input
            type="text"
            placeholder="sensor.wallonia_electricity_price"
            .value=${e.price_entity??""}
            @input=${t=>this._set("price_entity",t.target.value||void 0)}
          />
        </label>

        <label class="field">
          <span>Static price fallback (€/kWh, optional)</span>
          <input
            type="number"
            step="0.0001"
            placeholder="0.3783"
            .value=${e.price!==void 0?String(e.price):""}
            @input=${t=>{let r=t.target.value;this._set("price",r===""?void 0:Number(r))}}
          />
        </label>

        <label class="field toggle">
          <span>Use Home Assistant Energy price</span>
          <input
            type="checkbox"
            .checked=${e.use_energy_prefs??!1}
            @change=${t=>this._set("use_energy_prefs",t.target.checked)}
          />
        </label>

        <label class="field">
          <span>Curve lookback (hours)</span>
          <input
            type="number"
            min="1"
            max="24"
            .value=${String(e.curve_hours??4)}
            @input=${t=>this._set("curve_hours",Number(t.target.value))}
          />
        </label>

        ${It.map(t=>f`
            <label class="field toggle">
              <span>${t.label}</span>
              <input
                type="checkbox"
                .checked=${e[t.key]??!0}
                @change=${r=>this._set(t.key,r.target.checked)}
              />
            </label>
          `)}
      </div>
    `}_renderDevicePicker(e){return customElements.get("ha-device-picker")&&this.hass?f`
        <ha-device-picker
          .hass=${this.hass}
          .value=${e.device??""}
          .label=${"Wellborne device"}
          .includeDomains=${["wellborne"]}
          @value-changed=${t=>this._set("device",t.detail.value||void 0)}
        ></ha-device-picker>
      `:f`
      <label class="field">
        <span>Wellborne device id</span>
        <input
          type="text"
          .value=${e.device??""}
          @input=${t=>this._set("device",t.target.value||void 0)}
        />
      </label>
    `}_set(e,t){if(!this._config)return;let r={...this._config};t===void 0||t===""?delete r[e]:r[e]=t,this._config=r,this.dispatchEvent(new CustomEvent("config-changed",{detail:{config:r},bubbles:!0,composed:!0}))}};P.styles=D`
    .form {
      display: flex;
      flex-direction: column;
      gap: 12px;
      padding: 8px 0;
    }
    .field {
      display: flex;
      flex-direction: column;
      gap: 4px;
      font-size: 0.9rem;
      color: var(--primary-text-color, #e1e1e1);
    }
    .field.toggle {
      flex-direction: row;
      align-items: center;
      justify-content: space-between;
    }
    .field span {
      color: var(--secondary-text-color, #9b9b9b);
    }
    input[type='text'],
    input[type='number'] {
      padding: 8px;
      border-radius: 6px;
      border: 1px solid var(--divider-color, #444);
      background: var(--card-background-color, #2a2a2c);
      color: var(--primary-text-color, #e1e1e1);
      font: inherit;
    }
  `,S([ie({attribute:!1})],P.prototype,"hass",2),S([O()],P.prototype,"_config",2);customElements.get(Y)||customElements.define(Y,P)});L();$e();L();var Xe=D`
  :host {
    /* Theme-adaptive tokens with doc section-2 fallbacks. */
    --wb-surface: var(--ha-card-background, var(--card-background-color, #1c1c1e));
    --wb-primary: var(--primary-text-color, #e1e1e1);
    --wb-secondary: var(--secondary-text-color, #9b9b9b);
    --wb-divider: var(--divider-color, rgba(255, 255, 255, 0.12));
    --wb-accent: var(--wellborne-charging-color, var(--energy-solar-color, #0f9d58));
    --wb-error: var(--error-color, #db4437);
    /* Subtle fill used by pill chips / stat tiles (Mushroom-style). */
    --wb-chip-bg: color-mix(in srgb, var(--wb-primary) 8%, transparent);
    display: block;
  }

  ha-card {
    position: relative;
    padding: 16px;
    background: var(--wb-surface);
    overflow: hidden;
  }
  /* Status-tinted depth glow behind the hero; only visible while charging. */
  .card.charging::before {
    content: '';
    position: absolute;
    top: -40%;
    left: -10%;
    width: 70%;
    height: 80%;
    background: radial-gradient(
      circle at 30% 30%,
      color-mix(in srgb, var(--wb-accent) 22%, transparent),
      transparent 70%
    );
    pointer-events: none;
    z-index: 0;
  }
  .card > * {
    position: relative;
    z-index: 1;
  }

  .card.offline {
    opacity: 0.55;
  }

  /* ----- header ----- */
  .header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 12px;
  }
  .title {
    font-family: var(--ha-card-header-font-family, inherit);
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--wb-primary);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .header-right {
    display: flex;
    align-items: center;
    gap: 10px;
    flex: none;
  }
  .badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 0.8rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 12px;
    color: var(--wb-secondary);
    background: color-mix(in srgb, var(--wb-secondary) 16%, transparent);
  }
  .badge.charging {
    color: var(--wb-accent);
    background: color-mix(in srgb, var(--wb-accent) 18%, transparent);
  }
  .badge.offline {
    color: var(--wb-error);
    background: color-mix(in srgb, var(--wb-error) 18%, transparent);
  }
  .badge ha-icon {
    --mdc-icon-size: 16px;
  }
  .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--wb-secondary);
    flex: none;
  }
  .dot.online {
    background: var(--wb-accent);
  }
  .dot.offline {
    background: var(--wb-error);
  }

  /* ----- hero ----- */
  .hero {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .hero-main {
    flex: 1 1 auto;
    min-width: 0;
  }
  .live-row {
    display: flex;
    align-items: baseline;
    gap: 12px;
    margin-bottom: 4px;
  }
  .kw {
    font-size: 1.9rem;
    font-weight: 700;
    color: var(--wb-primary);
    font-variant-numeric: tabular-nums;
    line-height: 1.1;
  }
  .kw .unit {
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--wb-secondary);
    margin-left: 3px;
  }
  .duration {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--wb-secondary);
    font-variant-numeric: tabular-nums;
    margin-left: auto;
  }
  .ring-wrap {
    flex: none;
  }

  /* ----- curve ----- */
  .curve {
    position: relative;
    margin-top: 6px;
  }
  .curve-label {
    position: absolute;
    top: 0;
    left: 0;
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--wb-secondary);
    opacity: 0.7;
    pointer-events: none;
  }
  .curve-line {
    stroke: var(--wb-accent);
    stroke-width: 2;
    stroke-linejoin: round;
    stroke-linecap: round;
  }
  .card.offline .curve-line,
  .curve .idle .curve-line {
    stroke: var(--wb-secondary);
  }
  .curve-tip {
    fill: var(--wb-accent);
  }
  .curve-tip.static,
  .curve-tip.noanim {
    fill: var(--wb-secondary);
  }
  .curve-tip.live.animate {
    fill: var(--wb-accent);
    animation: wb-pulse 1.6s ease-out infinite;
    transform-box: fill-box;
    transform-origin: center;
  }
  @keyframes wb-pulse {
    0% {
      r: 2.6;
      opacity: 1;
    }
    70% {
      r: 5.5;
      opacity: 0.15;
    }
    100% {
      r: 2.6;
      opacity: 1;
    }
  }

  /* ----- chip row (Mushroom-style pills) ----- */
  .chips {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 6px;
    margin-top: 14px;
  }
  .chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--wb-primary);
    background: var(--wb-chip-bg);
    border-radius: 14px;
    padding: 4px 10px 4px 8px;
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
  }
  .chip ha-icon {
    --mdc-icon-size: 15px;
    color: var(--wb-secondary);
  }
  .chip.on {
    color: var(--wb-accent);
    background: color-mix(in srgb, var(--wb-accent) 14%, transparent);
  }
  .chip.on ha-icon {
    color: var(--wb-accent);
  }

  /* ----- footer block ----- */
  .footer {
    margin-top: 14px;
    padding-top: 14px;
    border-top: 1px solid var(--wb-divider);
  }
  .stats {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
  }
  .stat {
    display: flex;
    flex-direction: column;
    gap: 2px;
    background: var(--wb-chip-bg);
    border-radius: 12px;
    padding: 8px 12px;
  }
  .stat-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--wb-secondary);
  }
  .stat-value {
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--wb-primary);
    font-variant-numeric: tabular-nums;
    line-height: 1.1;
  }
  .stat-unit {
    font-size: 0.72rem;
    font-weight: 500;
    color: var(--wb-secondary);
    margin-left: 4px;
  }
  .last {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-top: 10px;
  }
  .last-info {
    display: flex;
    flex-direction: column;
    gap: 2px;
    min-width: 0;
  }
  .last-label {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--wb-secondary);
  }
  .last-label ha-icon {
    --mdc-icon-size: 14px;
  }
  .last-detail {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--wb-primary);
    font-variant-numeric: tabular-nums;
  }
  .last-cost {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    flex: none;
  }
  .last-cost-value {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--wb-accent);
    font-variant-numeric: tabular-nums;
    line-height: 1.1;
  }
  .last-cost-caption {
    font-size: 0.66rem;
    color: var(--wb-secondary);
    opacity: 0.85;
  }

  /* ----- SoC ring svg ----- */
  .soc-track {
    stroke: var(--wb-divider);
  }
  .soc-arc {
    stroke: var(--wb-accent);
  }
  .soc-arc.animate {
    transition: stroke-dasharray 280ms ease-out;
  }
  .soc-pct {
    fill: var(--wb-primary);
    font-size: 18px;
    font-weight: 700;
    font-variant-numeric: tabular-nums;
  }
  .soc-range {
    fill: var(--wb-secondary);
    font-size: 9px;
    font-weight: 600;
  }

  /* ----- responsive ----- */
  @media (max-width: 360px) {
    .hero {
      flex-direction: column-reverse;
      align-items: stretch;
    }
    .ring-wrap {
      align-self: center;
    }
    .duration {
      margin-left: auto;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .curve-tip.live.animate {
      animation: none;
    }
    .soc-arc.animate {
      transition: none;
    }
  }
`;Z();Z();function it(n,e){let t={},r=Object.keys(oe);for(let s of r){let o=e[`${s}_entity`];typeof o=="string"&&o.length>0&&(t[s]=o)}if(!e.device)return t;let i=Pt(n,e.device);if(n.entities&&i){for(let s of Object.values(n.entities))if(s.device_id===e.device&&s.platform===se&&s.unique_id)for(let o of r)t[o]||s.unique_id===`${i}_${oe[o]}`&&(t[o]=s.entity_id)}if(n.entities)for(let s of Object.values(n.entities))s.device_id===e.device&&rt(t,r,s.entity_id,s.platform);if(!n.entities)for(let s of Object.keys(n.states))rt(t,r,s);return t}function Pt(n,e){let t=n.devices?.[e];if(t){for(let r of t.identifiers)if(r[0]===se)return r[1]}}function rt(n,e,t,r){let i=t.indexOf(".");if(i<0)return;let s=t.slice(0,i),o=t.slice(i+1);for(let a of e){if(n[a])continue;let p=tt.has(a)?"binary_sensor":"sensor";if(s!==p||r&&r!==se)continue;let d=oe[a];Ht(o,d)&&(n[a]=t)}}function Ht(n,e){if(!n.endsWith(`_${e}`))return!1;let t=n.slice(0,n.length-e.length-1);return!(e==="current"&&(t.endsWith("_max")||t.includes("household"))||e==="energy"&&t.endsWith("_last_session"))}Z();async function nt(n,e){let t=Mt(n,e.price_entity);if(t!==null)return{price:t,source:"CREG"};if(typeof e.price=="number"&&Number.isFinite(e.price)&&e.price>0)return{price:e.price,source:"static"};if(e.use_energy_prefs){let r=await Lt(n);if(r!==null)return{price:r,source:"energy-prefs"}}return null}function Mt(n,e){if(!e)return null;let t=n.states[e];if(!t||$.has(t.state))return null;let r=Number(t.state);if(!Number.isFinite(r))return null;let i=String(t.attributes.unit_of_measurement??"").toLowerCase();return Nt(r,i)}function Nt(n,e){let t=e.replace(/\s+/g,"");return t.includes("/mwh")?n/1e3:t.includes("/wh")&&!t.includes("/kwh")?n*1e3:n}async function Lt(n){let e;try{e=await n.callWS({type:"energy/get_prefs"})}catch{return null}let r=e.energy_sources?.find(i=>i.type==="grid")?.flow_from?.[0];if(!r)return null;if(r.entity_energy_price){let i=n.states[r.entity_energy_price];if(i&&!$.has(i.state)){let s=Number(i.state);if(Number.isFinite(s))return s}}return typeof r.number_energy_price=="number"&&Number.isFinite(r.number_energy_price)?r.number_energy_price:null}function st(n,e){return n===null||!Number.isFinite(n)?null:n*e}function ot(n,e,t){let r=e.currency??n.config.currency??"EUR";try{return new Intl.NumberFormat(n.locale.language,{style:"currency",currency:r}).format(t)}catch{return`${t.toFixed(2)} ${r}`}}L();function Ot(n,e,t,r=2){let i=n.filter(u=>Number.isFinite(u.v));if(i.length===0)return{line:"",area:"",tip:null};if(i.length===1){let u=t/2;return{line:`M ${r} ${u} L ${e-r} ${u}`,area:`M ${r} ${u} L ${e-r} ${u} L ${e-r} ${t} L ${r} ${t} Z`,tip:{x:e-r,y:u}}}let s=i[0].t,a=i[i.length-1].t-s||1,c=-1/0,p=1/0;for(let u of i)u.v>c&&(c=u.v),u.v<p&&(p=u.v);p=Math.min(p,0);let d=c-p||1,h=e-r*2,_=t-r*2,g=i.map(u=>{let dt=r+(u.t-s)/a*h,ut=r+_-(u.v-p)/d*_;return{x:dt,y:ut}}),x=`M ${E(g[0].x)} ${E(g[0].y)}`;for(let u=1;u<g.length;u++)x+=` L ${E(g[u].x)} ${E(g[u].y)}`;let Ae=g[g.length-1],pt=g[0],ht=`${x} L ${E(Ae.x)} ${E(t)} L ${E(pt.x)} ${E(t)} Z`;return{line:x,area:ht,tip:Ae}}function E(n){return(Math.round(n*100)/100).toString()}function at(n,e){let{width:t,height:r,gradientId:i,animate:s,live:o}=e,a=Ot(n,t,r);if(!a.line)return A`<svg viewBox="0 0 ${t} ${r}" width="100%" height="${r}" aria-hidden="true"></svg>`;let c=a.tip?A`
        <circle
          class="curve-tip ${o?"live":"static"} ${s?"animate":"noanim"}"
          cx="${a.tip.x}"
          cy="${a.tip.y}"
          r="2.6"
        ></circle>`:l;return A`
    <svg viewBox="0 0 ${t} ${r}" width="100%" height="${r}" preserveAspectRatio="none" aria-hidden="true">
      <defs>
        <linearGradient id="${i}" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="var(--wb-accent)" stop-opacity="0.18"></stop>
          <stop offset="100%" stop-color="var(--wb-accent)" stop-opacity="0"></stop>
        </linearGradient>
      </defs>
      <path class="curve-area" d="${a.area}" fill="url(#${i})"></path>
      <path class="curve-line" d="${a.line}" fill="none"></path>
      ${c}
    </svg>
  `}L();function ct(n){let e=n.size??96,t=8,r=(e-t)/2,i=e/2,s=e/2,o=2*Math.PI*r,a=Ut(n.percent,0,100),c=a/100*o,p=n.animate?"soc-arc animate":"soc-arc";return A`
    <svg viewBox="0 0 ${e} ${e}" width="${e}" height="${e}" class="soc-ring" role="img"
         aria-label="State of charge ${Math.round(a)} percent">
      <circle class="soc-track" cx="${i}" cy="${s}" r="${r}" fill="none" stroke-width="${t}"></circle>
      <circle
        class="${p}"
        cx="${i}"
        cy="${s}"
        r="${r}"
        fill="none"
        stroke-width="${t}"
        stroke-linecap="round"
        stroke-dasharray="${c} ${o-c}"
        transform="rotate(-90 ${i} ${s})"
      ></circle>
      <text class="soc-pct" x="${i}" y="${n.rangeLabel?s-2:s+1}" text-anchor="middle" dominant-baseline="middle">${Math.round(a)}%</text>
      ${n.rangeLabel?A`<text class="soc-range" x="${i}" y="${s+14}" text-anchor="middle" dominant-baseline="middle">${n.rangeLabel}</text>`:A``}
    </svg>
  `}function Ut(n,e,t){return Math.min(t,Math.max(e,n))}we();var Dt=220,zt=56,H=class extends v{constructor(){super(...arguments);this._history=[];this._price=null;this._entities={};this._lastHistoryFetch=0;this._historyKey="";this._priceKey=""}static async getConfigElement(){return await Promise.resolve().then(()=>(we(),lt)),document.createElement(Y)}static getStubConfig(){return{type:`custom:${V}`,device:"",...xe}}getCardSize(){return 4}setConfig(t){if(!t)throw new Error("Invalid configuration");this._config={...xe,...t}}set hass(t){this._hass=t,this._config&&(this._entities=it(t,this._config),this._maybeFetchHistory(),this._maybeResolvePrice(),this.requestUpdate())}get hass(){return this._hass}_maybeResolvePrice(){if(!this._hass||!this._config.show_cost)return;let t=`${this._config.price_entity??""}|${this._config.price??""}|${this._config.use_energy_prefs??""}|${this._priceEntityState()}`;t!==this._priceKey&&(this._priceKey=t,nt(this._hass,this._config).then(r=>{this._price=r}).catch(()=>{this._price=null}))}_priceEntityState(){let t=this._config.price_entity;return!t||!this._hass?"":this._hass.states[t]?.state??""}_maybeFetchHistory(){if(!this._hass||!this._config.show_curve)return;let t=this._entities.power;if(!t)return;let r=Date.now();if(!(t!==this._historyKey)&&r-this._lastHistoryFetch<25e3)return;this._historyKey=t,this._lastHistoryFetch=r;let s=this._config.curve_hours??4,o=new Date(r-s*36e5).toISOString(),a=`history/period/${encodeURIComponent(o)}?filter_entity_id=${encodeURIComponent(t)}&minimal_response&no_attributes`;this._hass.callApi("GET",a).then(c=>{this._history=this._parseHistory(c,t)}).catch(()=>{this._history=[]})}_parseHistory(t,r){let i=Array.isArray(t)?t.find(o=>o[0]?.entity_id===r)??t[0]:void 0;if(!i)return[];let s=[];for(let o of i){let a=Number(o.state);if(!Number.isFinite(a))continue;let c=o.last_changed??o.last_updated;s.push({t:c?Date.parse(c):Date.now(),v:a})}return s}_stateOf(t){let r=this._entities[t];if(!(!r||!this._hass))return this._hass.states[r]}_num(t){let r=this._stateOf(t);if(!r||$.has(r.state))return null;let i=Number(r.state);return Number.isFinite(i)?i:null}_str(t){let r=this._stateOf(t);return!r||$.has(r.state)?null:r.state}_bool(t){let r=this._stateOf(t);return!r||$.has(r.state)?null:r.state==="on"}_cardState(){if(this._bool("charger_online")===!1)return"offline";let r=this._bool("charging"),i=this._str("status");return r===!0||i==="charging"?"charging":"idle"}render(){if(!this._config||!this._hass)return l;let t=this._cardState(),r=this._config.name??this._hass.devices?.[this._config.device??""]?.name??"Wellborne Charger";return f`
      <ha-card @click=${this._handleTap}>
        <div class="card ${t}">
          ${this._renderHeader(r,t)}
          ${this._renderHero(t)}
          ${this._config.show_curve?this._renderCurveBlock(t):l}
          ${this._renderChips(t)}
          ${this._renderFooter()}
        </div>
      </ha-card>
    `}_renderHeader(t,r){let i=r!=="offline",s=r==="charging"?f`<span class="badge charging"><ha-icon icon="mdi:lightning-bolt"></ha-icon>Charging</span>`:r==="offline"?f`<span class="badge offline"><ha-icon icon="mdi:cloud-off-outline"></ha-icon>Offline</span>`:f`<span class="badge"><ha-icon icon="mdi:sleep"></ha-icon>Idle</span>`;return f`
      <div class="header">
        <div class="title">${t}</div>
        <div class="header-right">
          ${s}
          <span class="dot ${i?"online":"offline"}" title=${i?"online":"offline"}></span>
        </div>
      </div>
    `}_renderHero(t){let r=t==="offline",i=this._num("power"),s=r||i===null?y:(i/1e3).toFixed(1),o=r?y:this._formatDuration(this._num("session_duration"));return f`
      <div class="hero">
        ${this._renderRing(t)}
        <div class="hero-main">
          <div class="live-row">
            <div class="kw">${s}<span class="unit">${s===y?"":"kW"}</span></div>
            <div class="duration">${o}</div>
          </div>
        </div>
      </div>
    `}_renderRing(t){let r=this._config.battery_entity;if(!r||!this._hass)return l;let i=this._hass.states[r];if(!i||$.has(i.state))return l;let s=Number(i.state);if(!Number.isFinite(s))return l;let o=this._rangeLabel(t);return f`
      <div class="ring-wrap">
        ${ct({percent:s,rangeLabel:o,animate:!this._reducedMotion()})}
      </div>
    `}_rangeLabel(t){if(t==="offline")return;let r=this._config.range_entity;if(r&&this._hass){let s=this._hass.states[r];if(s&&!$.has(s.state)&&Number.isFinite(Number(s.state)))return`${Math.round(Number(s.state))} km`}let i=this._num("added_range");return i===null?void 0:`+${Math.round(i)} km`}_renderCurveBlock(t){let r=t==="charging";return f`
      <div class="curve ${t}">
        <span class="curve-label">${r?"Live power":"Last session"}</span>
        ${at(this._history,{width:Dt,height:zt,gradientId:"wb-curve-grad",animate:!this._reducedMotion(),live:r})}
      </div>
    `}_chip(t,r,i=!1){return f`<span class="chip ${i?"on":""}"><ha-icon icon=${t}></ha-icon>${r}</span>`}_renderChips(t){let r=t==="offline",i=this._bool("vehicle_connected"),s=r?null:this._num("current"),o=r?null:this._num("energy"),a=r?null:this._num("added_range"),c=i===!0?this._chip("mdi:power-plug","Connected",!0):this._chip("mdi:power-plug-outline",y);return f`
      <div class="chips">
        ${c} ${this._chip("mdi:current-ac",s===null?y:`${s.toFixed(0)} A`)}
        ${this._chip("mdi:lightning-bolt",o===null?y:`${o.toFixed(1)} kWh`)}
        ${this._chip("mdi:map-marker-distance",a===null?y:`+${Math.round(a)} km`)}
      </div>
    `}_renderFooter(){let t=this._config.show_totals,r=this._config.show_cost;return!t&&!r?l:f`
      <div class="footer">
        ${t?this._renderTotals():l}
        ${r?this._renderLastCharge():l}
      </div>
    `}_renderTotals(){let t=this._num("monthly_energy"),r=this._num("yearly_energy");return f`
      <div class="stats">
        <div class="stat">
          <span class="stat-label">This month</span>
          <span class="stat-value">${t===null?y:`${this._fmtKwh(t)}`}<span class="stat-unit">kWh</span></span>
        </div>
        <div class="stat">
          <span class="stat-label">This year</span>
          <span class="stat-value">${r===null?y:`${this._fmtKwh(r)}`}<span class="stat-unit">kWh</span></span>
        </div>
      </div>
    `}_renderLastCharge(){let t=this._num("last_session_energy"),r=this._num("last_session_duration"),s=`${t===null?y:`${this._fmtKwh(t)} kWh`} \xB7 ${this._formatDuration(r)}`,o=this._price===null?null:st(t,this._price.price);if(o===null)return f`
        <div class="last">
          <div class="last-info">
            <span class="last-label"><ha-icon icon="mdi:history"></ha-icon>Last charge</span>
            <span class="last-detail">${s}</span>
          </div>
        </div>
      `;let a=ot(this._hass,this._config,o),c=this._price.source;return f`
      <div class="last">
        <div class="last-info">
          <span class="last-label"><ha-icon icon="mdi:history"></ha-icon>Last charge</span>
          <span class="last-detail">${s}</span>
        </div>
        <div class="last-cost">
          <span class="last-cost-value">~${a}</span>
          <span class="last-cost-caption">est. · ${c}</span>
        </div>
      </div>
    `}_formatDuration(t){if(t===null||!Number.isFinite(t)||t<0)return y;let r=Math.floor(t/60),i=Math.round(t%60);return`${r}:${i.toString().padStart(2,"0")}`}_fmtKwh(t){return new Intl.NumberFormat(this._hass.locale.language,{maximumFractionDigits:1}).format(t)}_reducedMotion(){return typeof window<"u"&&typeof window.matchMedia=="function"&&window.matchMedia("(prefers-reduced-motion: reduce)").matches}_handleTap(){let t=this._entities.status??this._entities.power??this._entities.charger_online;t&&this.dispatchEvent(new CustomEvent("hass-more-info",{detail:{entityId:t},bubbles:!0,composed:!0}))}};H.styles=Xe,S([O()],H.prototype,"_config",2),S([O()],H.prototype,"_history",2),S([O()],H.prototype,"_price",2);customElements.get(V)||customElements.define(V,H);window.customCards=window.customCards??[];window.customCards.push({type:V,name:"Wellborne Charger Card",description:"Monitoring card for the Wellborne EV charger (live status, energy, cost).",preview:!0,documentationURL:"https://github.com/your/repo/tree/main/charger-card"});console.info(`%c WELLBORNE-CHARGER-CARD %c v${et} `,"background:#0f9d58;color:#fff","");export{H as WellborneChargerCard};
/*! Bundled license information:

@lit/reactive-element/css-tag.js:
  (**
   * @license
   * Copyright 2019 Google LLC
   * SPDX-License-Identifier: BSD-3-Clause
   *)

@lit/reactive-element/reactive-element.js:
  (**
   * @license
   * Copyright 2017 Google LLC
   * SPDX-License-Identifier: BSD-3-Clause
   *)

lit-html/lit-html.js:
  (**
   * @license
   * Copyright 2017 Google LLC
   * SPDX-License-Identifier: BSD-3-Clause
   *)

lit-element/lit-element.js:
  (**
   * @license
   * Copyright 2017 Google LLC
   * SPDX-License-Identifier: BSD-3-Clause
   *)

lit-html/is-server.js:
  (**
   * @license
   * Copyright 2022 Google LLC
   * SPDX-License-Identifier: BSD-3-Clause
   *)

@lit/reactive-element/decorators/custom-element.js:
  (**
   * @license
   * Copyright 2017 Google LLC
   * SPDX-License-Identifier: BSD-3-Clause
   *)

@lit/reactive-element/decorators/property.js:
  (**
   * @license
   * Copyright 2017 Google LLC
   * SPDX-License-Identifier: BSD-3-Clause
   *)

@lit/reactive-element/decorators/state.js:
  (**
   * @license
   * Copyright 2017 Google LLC
   * SPDX-License-Identifier: BSD-3-Clause
   *)

@lit/reactive-element/decorators/event-options.js:
  (**
   * @license
   * Copyright 2017 Google LLC
   * SPDX-License-Identifier: BSD-3-Clause
   *)

@lit/reactive-element/decorators/base.js:
  (**
   * @license
   * Copyright 2017 Google LLC
   * SPDX-License-Identifier: BSD-3-Clause
   *)

@lit/reactive-element/decorators/query.js:
  (**
   * @license
   * Copyright 2017 Google LLC
   * SPDX-License-Identifier: BSD-3-Clause
   *)

@lit/reactive-element/decorators/query-all.js:
  (**
   * @license
   * Copyright 2017 Google LLC
   * SPDX-License-Identifier: BSD-3-Clause
   *)

@lit/reactive-element/decorators/query-async.js:
  (**
   * @license
   * Copyright 2017 Google LLC
   * SPDX-License-Identifier: BSD-3-Clause
   *)

@lit/reactive-element/decorators/query-assigned-elements.js:
  (**
   * @license
   * Copyright 2021 Google LLC
   * SPDX-License-Identifier: BSD-3-Clause
   *)

@lit/reactive-element/decorators/query-assigned-nodes.js:
  (**
   * @license
   * Copyright 2017 Google LLC
   * SPDX-License-Identifier: BSD-3-Clause
   *)
*/
