var St=Object.defineProperty;var fe=Object.getOwnPropertyDescriptor;var m=(n,t)=>()=>(n&&(t=n(n=0)),t);var me=(n,t)=>{for(var e in t)St(n,e,{get:t[e],enumerable:!0})};var S=(n,t,e,i)=>{for(var s=i>1?void 0:i?fe(t,e):t,r=n.length-1,o;r>=0;r--)(o=n[r])&&(s=(i?o(t,e,s):o(s))||s);return i&&s&&St(t,e,s),s};var J,Q,at,Ct,I,kt,D,Rt,ct,lt=m(()=>{J=globalThis,Q=J.ShadowRoot&&(J.ShadyCSS===void 0||J.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,at=Symbol(),Ct=new WeakMap,I=class{constructor(t,e,i){if(this._$cssResult$=!0,i!==at)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t,this.t=e}get styleSheet(){let t=this.o,e=this.t;if(Q&&t===void 0){let i=e!==void 0&&e.length===1;i&&(t=Ct.get(e)),t===void 0&&((this.o=t=new CSSStyleSheet).replaceSync(this.cssText),i&&Ct.set(e,t))}return t}toString(){return this.cssText}},kt=n=>new I(typeof n=="string"?n:n+"",void 0,at),D=(n,...t)=>{let e=n.length===1?n[0]:t.reduce((i,s,r)=>i+(o=>{if(o._$cssResult$===!0)return o.cssText;if(typeof o=="number")return o;throw Error("Value passed to 'css' function must be a 'css' function result: "+o+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(s)+n[r+1],n[0]);return new I(e,n,at)},Rt=(n,t)=>{if(Q)n.adoptedStyleSheets=t.map(e=>e instanceof CSSStyleSheet?e:e.styleSheet);else for(let e of t){let i=document.createElement("style"),s=J.litNonce;s!==void 0&&i.setAttribute("nonce",s),i.textContent=e.cssText,n.appendChild(i)}},ct=Q?n=>n:n=>n instanceof CSSStyleSheet?(t=>{let e="";for(let i of t.cssRules)e+=i.cssText;return kt(e)})(n):n});var ge,_e,ye,ve,be,$e,X,Tt,xe,we,z,W,tt,Pt,b,j=m(()=>{lt();lt();({is:ge,defineProperty:_e,getOwnPropertyDescriptor:ye,getOwnPropertyNames:ve,getOwnPropertySymbols:be,getPrototypeOf:$e}=Object),X=globalThis,Tt=X.trustedTypes,xe=Tt?Tt.emptyScript:"",we=X.reactiveElementPolyfillSupport,z=(n,t)=>n,W={toAttribute(n,t){switch(t){case Boolean:n=n?xe:null;break;case Object:case Array:n=n==null?n:JSON.stringify(n)}return n},fromAttribute(n,t){let e=n;switch(t){case Boolean:e=n!==null;break;case Number:e=n===null?null:Number(n);break;case Object:case Array:try{e=JSON.parse(n)}catch{e=null}}return e}},tt=(n,t)=>!ge(n,t),Pt={attribute:!0,type:String,converter:W,reflect:!1,useDefault:!1,hasChanged:tt};Symbol.metadata??=Symbol("metadata"),X.litPropertyMetadata??=new WeakMap;b=class extends HTMLElement{static addInitializer(t){this._$Ei(),(this.l??=[]).push(t)}static get observedAttributes(){return this.finalize(),this._$Eh&&[...this._$Eh.keys()]}static createProperty(t,e=Pt){if(e.state&&(e.attribute=!1),this._$Ei(),this.prototype.hasOwnProperty(t)&&((e=Object.create(e)).wrapped=!0),this.elementProperties.set(t,e),!e.noAccessor){let i=Symbol(),s=this.getPropertyDescriptor(t,i,e);s!==void 0&&_e(this.prototype,t,s)}}static getPropertyDescriptor(t,e,i){let{get:s,set:r}=ye(this.prototype,t)??{get(){return this[e]},set(o){this[e]=o}};return{get:s,set(o){let c=s?.call(this);r?.call(this,o),this.requestUpdate(t,c,i)},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)??Pt}static _$Ei(){if(this.hasOwnProperty(z("elementProperties")))return;let t=$e(this);t.finalize(),t.l!==void 0&&(this.l=[...t.l]),this.elementProperties=new Map(t.elementProperties)}static finalize(){if(this.hasOwnProperty(z("finalized")))return;if(this.finalized=!0,this._$Ei(),this.hasOwnProperty(z("properties"))){let e=this.properties,i=[...ve(e),...be(e)];for(let s of i)this.createProperty(s,e[s])}let t=this[Symbol.metadata];if(t!==null){let e=litPropertyMetadata.get(t);if(e!==void 0)for(let[i,s]of e)this.elementProperties.set(i,s)}this._$Eh=new Map;for(let[e,i]of this.elementProperties){let s=this._$Eu(e,i);s!==void 0&&this._$Eh.set(s,e)}this.elementStyles=this.finalizeStyles(this.styles)}static finalizeStyles(t){let e=[];if(Array.isArray(t)){let i=new Set(t.flat(1/0).reverse());for(let s of i)e.unshift(ct(s))}else t!==void 0&&e.push(ct(t));return e}static _$Eu(t,e){let i=e.attribute;return i===!1?void 0:typeof i=="string"?i:typeof t=="string"?t.toLowerCase():void 0}constructor(){super(),this._$Ep=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Em=null,this._$Ev()}_$Ev(){this._$ES=new Promise(t=>this.enableUpdating=t),this._$AL=new Map,this._$E_(),this.requestUpdate(),this.constructor.l?.forEach(t=>t(this))}addController(t){(this._$EO??=new Set).add(t),this.renderRoot!==void 0&&this.isConnected&&t.hostConnected?.()}removeController(t){this._$EO?.delete(t)}_$E_(){let t=new Map,e=this.constructor.elementProperties;for(let i of e.keys())this.hasOwnProperty(i)&&(t.set(i,this[i]),delete this[i]);t.size>0&&(this._$Ep=t)}createRenderRoot(){let t=this.shadowRoot??this.attachShadow(this.constructor.shadowRootOptions);return Rt(t,this.constructor.elementStyles),t}connectedCallback(){this.renderRoot??=this.createRenderRoot(),this.enableUpdating(!0),this._$EO?.forEach(t=>t.hostConnected?.())}enableUpdating(t){}disconnectedCallback(){this._$EO?.forEach(t=>t.hostDisconnected?.())}attributeChangedCallback(t,e,i){this._$AK(t,i)}_$ET(t,e){let i=this.constructor.elementProperties.get(t),s=this.constructor._$Eu(t,i);if(s!==void 0&&i.reflect===!0){let r=(i.converter?.toAttribute!==void 0?i.converter:W).toAttribute(e,i.type);this._$Em=t,r==null?this.removeAttribute(s):this.setAttribute(s,r),this._$Em=null}}_$AK(t,e){let i=this.constructor,s=i._$Eh.get(t);if(s!==void 0&&this._$Em!==s){let r=i.getPropertyOptions(s),o=typeof r.converter=="function"?{fromAttribute:r.converter}:r.converter?.fromAttribute!==void 0?r.converter:W;this._$Em=s;let c=o.fromAttribute(e,r.type);this[s]=c??this._$Ej?.get(s)??c,this._$Em=null}}requestUpdate(t,e,i,s=!1,r){if(t!==void 0){let o=this.constructor;if(s===!1&&(r=this[t]),i??=o.getPropertyOptions(t),!((i.hasChanged??tt)(r,e)||i.useDefault&&i.reflect&&r===this._$Ej?.get(t)&&!this.hasAttribute(o._$Eu(t,i))))return;this.C(t,e,i)}this.isUpdatePending===!1&&(this._$ES=this._$EP())}C(t,e,{useDefault:i,reflect:s,wrapped:r},o){i&&!(this._$Ej??=new Map).has(t)&&(this._$Ej.set(t,o??e??this[t]),r!==!0||o!==void 0)||(this._$AL.has(t)||(this.hasUpdated||i||(e=void 0),this._$AL.set(t,e)),s===!0&&this._$Em!==t&&(this._$Eq??=new Set).add(t))}async _$EP(){this.isUpdatePending=!0;try{await this._$ES}catch(e){Promise.reject(e)}let t=this.scheduleUpdate();return t!=null&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){if(!this.isUpdatePending)return;if(!this.hasUpdated){if(this.renderRoot??=this.createRenderRoot(),this._$Ep){for(let[s,r]of this._$Ep)this[s]=r;this._$Ep=void 0}let i=this.constructor.elementProperties;if(i.size>0)for(let[s,r]of i){let{wrapped:o}=r,c=this[s];o!==!0||this._$AL.has(s)||c===void 0||this.C(s,void 0,r,c)}}let t=!1,e=this._$AL;try{t=this.shouldUpdate(e),t?(this.willUpdate(e),this._$EO?.forEach(i=>i.hostUpdate?.()),this.update(e)):this._$EM()}catch(i){throw t=!1,this._$EM(),i}t&&this._$AE(e)}willUpdate(t){}_$AE(t){this._$EO?.forEach(e=>e.hostUpdated?.()),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t)}_$EM(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$ES}shouldUpdate(t){return!0}update(t){this._$Eq&&=this._$Eq.forEach(e=>this._$ET(e,this[e])),this._$EM()}updated(t){}firstUpdated(t){}};b.elementStyles=[],b.shadowRootOptions={mode:"open"},b[z("elementProperties")]=new Map,b[z("finalized")]=new Map,we?.({ReactiveElement:b}),(X.reactiveElementVersions??=[]).push("2.1.2")});function jt(n,t){if(!_t(n)||!n.hasOwnProperty("raw"))throw Error("invalid template strings array");return Mt!==void 0?Mt.createHTML(t):t}function M(n,t,e=n,i){if(t===T)return t;let s=i!==void 0?e._$Co?.[i]:e._$Cl,r=B(t)?void 0:t._$litDirective$;return s?.constructor!==r&&(s?._$AO?.(!1),r===void 0?s=void 0:(s=new r(n),s._$AT(n,e,i)),i!==void 0?(e._$Co??=[])[i]=s:e._$Cl=s),s!==void 0&&(t=M(n,s._$AS(n,t.values),s,i)),t}var gt,Ht,et,Mt,Dt,w,zt,Ae,R,K,B,_t,Ee,pt,F,Nt,Lt,C,Ot,Ut,Wt,yt,f,A,qe,T,p,It,k,Se,q,ht,G,N,ut,dt,ft,mt,Ce,Ft,it=m(()=>{gt=globalThis,Ht=n=>n,et=gt.trustedTypes,Mt=et?et.createPolicy("lit-html",{createHTML:n=>n}):void 0,Dt="$lit$",w=`lit$${Math.random().toFixed(9).slice(2)}$`,zt="?"+w,Ae=`<${zt}>`,R=document,K=()=>R.createComment(""),B=n=>n===null||typeof n!="object"&&typeof n!="function",_t=Array.isArray,Ee=n=>_t(n)||typeof n?.[Symbol.iterator]=="function",pt=`[ 	
\f\r]`,F=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,Nt=/-->/g,Lt=/>/g,C=RegExp(`>|${pt}(?:([^\\s"'>=/]+)(${pt}*=${pt}*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`,"g"),Ot=/'/g,Ut=/"/g,Wt=/^(?:script|style|textarea|title)$/i,yt=n=>(t,...e)=>({_$litType$:n,strings:t,values:e}),f=yt(1),A=yt(2),qe=yt(3),T=Symbol.for("lit-noChange"),p=Symbol.for("lit-nothing"),It=new WeakMap,k=R.createTreeWalker(R,129);Se=(n,t)=>{let e=n.length-1,i=[],s,r=t===2?"<svg>":t===3?"<math>":"",o=F;for(let c=0;c<e;c++){let a=n[c],l,u,h=-1,_=0;for(;_<a.length&&(o.lastIndex=_,u=o.exec(a),u!==null);)_=o.lastIndex,o===F?u[1]==="!--"?o=Nt:u[1]!==void 0?o=Lt:u[2]!==void 0?(Wt.test(u[2])&&(s=RegExp("</"+u[2],"g")),o=C):u[3]!==void 0&&(o=C):o===C?u[0]===">"?(o=s??F,h=-1):u[1]===void 0?h=-2:(h=o.lastIndex-u[2].length,l=u[1],o=u[3]===void 0?C:u[3]==='"'?Ut:Ot):o===Ut||o===Ot?o=C:o===Nt||o===Lt?o=F:(o=C,s=void 0);let g=o===C&&n[c+1].startsWith("/>")?" ":"";r+=o===F?a+Ae:h>=0?(i.push(l),a.slice(0,h)+Dt+a.slice(h)+w+g):a+w+(h===-2?c:g)}return[jt(n,r+(n[e]||"<?>")+(t===2?"</svg>":t===3?"</math>":"")),i]},q=class n{constructor({strings:t,_$litType$:e},i){let s;this.parts=[];let r=0,o=0,c=t.length-1,a=this.parts,[l,u]=Se(t,e);if(this.el=n.createElement(l,i),k.currentNode=this.el.content,e===2||e===3){let h=this.el.content.firstChild;h.replaceWith(...h.childNodes)}for(;(s=k.nextNode())!==null&&a.length<c;){if(s.nodeType===1){if(s.hasAttributes())for(let h of s.getAttributeNames())if(h.endsWith(Dt)){let _=u[o++],g=s.getAttribute(h).split(w),x=/([.?@])?(.*)/.exec(_);a.push({type:1,index:r,name:x[2],strings:g,ctor:x[1]==="."?ut:x[1]==="?"?dt:x[1]==="@"?ft:N}),s.removeAttribute(h)}else h.startsWith(w)&&(a.push({type:6,index:r}),s.removeAttribute(h));if(Wt.test(s.tagName)){let h=s.textContent.split(w),_=h.length-1;if(_>0){s.textContent=et?et.emptyScript:"";for(let g=0;g<_;g++)s.append(h[g],K()),k.nextNode(),a.push({type:2,index:++r});s.append(h[_],K())}}}else if(s.nodeType===8)if(s.data===zt)a.push({type:2,index:r});else{let h=-1;for(;(h=s.data.indexOf(w,h+1))!==-1;)a.push({type:7,index:r}),h+=w.length-1}r++}}static createElement(t,e){let i=R.createElement("template");return i.innerHTML=t,i}};ht=class{constructor(t,e){this._$AV=[],this._$AN=void 0,this._$AD=t,this._$AM=e}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(t){let{el:{content:e},parts:i}=this._$AD,s=(t?.creationScope??R).importNode(e,!0);k.currentNode=s;let r=k.nextNode(),o=0,c=0,a=i[0];for(;a!==void 0;){if(o===a.index){let l;a.type===2?l=new G(r,r.nextSibling,this,t):a.type===1?l=new a.ctor(r,a.name,a.strings,this,t):a.type===6&&(l=new mt(r,this,t)),this._$AV.push(l),a=i[++c]}o!==a?.index&&(r=k.nextNode(),o++)}return k.currentNode=R,s}p(t){let e=0;for(let i of this._$AV)i!==void 0&&(i.strings!==void 0?(i._$AI(t,i,e),e+=i.strings.length-2):i._$AI(t[e])),e++}},G=class n{get _$AU(){return this._$AM?._$AU??this._$Cv}constructor(t,e,i,s){this.type=2,this._$AH=p,this._$AN=void 0,this._$AA=t,this._$AB=e,this._$AM=i,this.options=s,this._$Cv=s?.isConnected??!0}get parentNode(){let t=this._$AA.parentNode,e=this._$AM;return e!==void 0&&t?.nodeType===11&&(t=e.parentNode),t}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(t,e=this){t=M(this,t,e),B(t)?t===p||t==null||t===""?(this._$AH!==p&&this._$AR(),this._$AH=p):t!==this._$AH&&t!==T&&this._(t):t._$litType$!==void 0?this.$(t):t.nodeType!==void 0?this.T(t):Ee(t)?this.k(t):this._(t)}O(t){return this._$AA.parentNode.insertBefore(t,this._$AB)}T(t){this._$AH!==t&&(this._$AR(),this._$AH=this.O(t))}_(t){this._$AH!==p&&B(this._$AH)?this._$AA.nextSibling.data=t:this.T(R.createTextNode(t)),this._$AH=t}$(t){let{values:e,_$litType$:i}=t,s=typeof i=="number"?this._$AC(t):(i.el===void 0&&(i.el=q.createElement(jt(i.h,i.h[0]),this.options)),i);if(this._$AH?._$AD===s)this._$AH.p(e);else{let r=new ht(s,this),o=r.u(this.options);r.p(e),this.T(o),this._$AH=r}}_$AC(t){let e=It.get(t.strings);return e===void 0&&It.set(t.strings,e=new q(t)),e}k(t){_t(this._$AH)||(this._$AH=[],this._$AR());let e=this._$AH,i,s=0;for(let r of t)s===e.length?e.push(i=new n(this.O(K()),this.O(K()),this,this.options)):i=e[s],i._$AI(r),s++;s<e.length&&(this._$AR(i&&i._$AB.nextSibling,s),e.length=s)}_$AR(t=this._$AA.nextSibling,e){for(this._$AP?.(!1,!0,e);t!==this._$AB;){let i=Ht(t).nextSibling;Ht(t).remove(),t=i}}setConnected(t){this._$AM===void 0&&(this._$Cv=t,this._$AP?.(t))}},N=class{get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}constructor(t,e,i,s,r){this.type=1,this._$AH=p,this._$AN=void 0,this.element=t,this.name=e,this._$AM=s,this.options=r,i.length>2||i[0]!==""||i[1]!==""?(this._$AH=Array(i.length-1).fill(new String),this.strings=i):this._$AH=p}_$AI(t,e=this,i,s){let r=this.strings,o=!1;if(r===void 0)t=M(this,t,e,0),o=!B(t)||t!==this._$AH&&t!==T,o&&(this._$AH=t);else{let c=t,a,l;for(t=r[0],a=0;a<r.length-1;a++)l=M(this,c[i+a],e,a),l===T&&(l=this._$AH[a]),o||=!B(l)||l!==this._$AH[a],l===p?t=p:t!==p&&(t+=(l??"")+r[a+1]),this._$AH[a]=l}o&&!s&&this.j(t)}j(t){t===p?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,t??"")}},ut=class extends N{constructor(){super(...arguments),this.type=3}j(t){this.element[this.name]=t===p?void 0:t}},dt=class extends N{constructor(){super(...arguments),this.type=4}j(t){this.element.toggleAttribute(this.name,!!t&&t!==p)}},ft=class extends N{constructor(t,e,i,s,r){super(t,e,i,s,r),this.type=5}_$AI(t,e=this){if((t=M(this,t,e,0)??p)===T)return;let i=this._$AH,s=t===p&&i!==p||t.capture!==i.capture||t.once!==i.once||t.passive!==i.passive,r=t!==p&&(i===p||s);s&&this.element.removeEventListener(this.name,this,i),r&&this.element.addEventListener(this.name,this,t),this._$AH=t}handleEvent(t){typeof this._$AH=="function"?this._$AH.call(this.options?.host??this.element,t):this._$AH.handleEvent(t)}},mt=class{constructor(t,e,i){this.element=t,this.type=6,this._$AN=void 0,this._$AM=e,this.options=i}get _$AU(){return this._$AM._$AU}_$AI(t){M(this,t)}},Ce=gt.litHtmlPolyfillSupport;Ce?.(q,G),(gt.litHtmlVersions??=[]).push("3.3.3");Ft=(n,t,e)=>{let i=e?.renderBefore??t,s=i._$litPart$;if(s===void 0){let r=e?.renderBefore??null;i._$litPart$=s=new G(t.insertBefore(K(),r),r,void 0,e??{})}return s._$AI(n),s}});var vt,v,ke,Kt=m(()=>{j();j();it();it();vt=globalThis,v=class extends b{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){let t=super.createRenderRoot();return this.renderOptions.renderBefore??=t.firstChild,t}update(t){let e=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Do=Ft(e,this.renderRoot,this.renderOptions)}connectedCallback(){super.connectedCallback(),this._$Do?.setConnected(!0)}disconnectedCallback(){super.disconnectedCallback(),this._$Do?.setConnected(!1)}render(){return T}};v._$litElement$=!0,v.finalized=!0,vt.litElementHydrateSupport?.({LitElement:v});ke=vt.litElementPolyfillSupport;ke?.({LitElement:v});(vt.litElementVersions??=[]).push("4.2.2")});var Bt=m(()=>{});var L=m(()=>{j();it();Kt();Bt()});var qt=m(()=>{});function st(n){return(t,e)=>typeof e=="object"?Te(n,t,e):((i,s,r)=>{let o=s.hasOwnProperty(r);return s.constructor.createProperty(r,i),o?Object.getOwnPropertyDescriptor(s,r):void 0})(n,t,e)}var Re,Te,bt=m(()=>{j();Re={attribute:!0,type:String,converter:W,reflect:!1,hasChanged:tt},Te=(n=Re,t,e)=>{let{kind:i,metadata:s}=e,r=globalThis.litPropertyMetadata.get(s);if(r===void 0&&globalThis.litPropertyMetadata.set(s,r=new Map),i==="setter"&&((n=Object.create(n)).wrapped=!0),r.set(e.name,n),i==="accessor"){let{name:o}=e;return{set(c){let a=t.get.call(this);t.set.call(this,c),this.requestUpdate(o,a,n,!0,c)},init(c){return c!==void 0&&this.C(o,void 0,n,c),c}}}if(i==="setter"){let{name:o}=e;return function(c){let a=this[o];t.call(this,c),this.requestUpdate(o,a,n,!0,c)}}throw Error("Unsupported decorator location: "+i)}});function O(n){return st({...n,state:!0,attribute:!1})}var Gt=m(()=>{bt();});var Vt=m(()=>{});var U=m(()=>{});var Yt=m(()=>{U();});var Zt=m(()=>{U();});var Jt=m(()=>{U();});var Qt=m(()=>{U();});var Xt=m(()=>{U();});var $t=m(()=>{qt();bt();Gt();Vt();Yt();Zt();Jt();Qt();Xt()});var V,Y,ee,rt,ot,ie,$,y,xt,Z=m(()=>{"use strict";V="wellborne-charger-card",Y="wellborne-charger-card-editor",ee="1.0.0",rt="wellborne",ot={power:"power",energy:"energy",current:"current",max_current:"max_current",session_duration:"session_duration",status:"status",added_range:"added_range",monthly_energy:"monthly_energy",yearly_energy:"yearly_energy",last_session_energy:"last_session_energy",last_session_duration:"last_session_duration",session_cost:"session_cost",wifi_ssid:"wifi_ssid",charging:"charging",charger_online:"charger_online",vehicle_connected:"vehicle_connected"},ie=new Set(["charging","charger_online","vehicle_connected"]),$=new Set(["unavailable","unknown","none",""]),y="\u2014",xt={show_curve:!0,show_totals:!0,show_cost:!0,curve_hours:4}});var le={};me(le,{WellborneChargerCardEditor:()=>P});var Ie,P,At=m(()=>{"use strict";L();$t();Z();Ie=[{key:"show_curve",label:"Power curve (sparkline)"},{key:"show_totals",label:"Month / year totals"},{key:"show_cost",label:"Last-charge cost"}],P=class extends v{setConfig(t){this._config=t}render(){if(!this._config)return p;let t=this._config;return f`
      <div class="form">
        ${this._renderDevicePicker(t)}

        <label class="field">
          <span>Name (optional)</span>
          <input
            type="text"
            .value=${t.name??""}
            @input=${e=>this._set("name",e.target.value||void 0)}
          />
        </label>

        <label class="field">
          <span>Battery entity (car SoC, optional)</span>
          <input
            type="text"
            placeholder="sensor.ioniq5_battery_level"
            .value=${t.battery_entity??""}
            @input=${e=>this._set("battery_entity",e.target.value||void 0)}
          />
        </label>

        <label class="field">
          <span>Price entity (€/kWh, optional)</span>
          <input
            type="text"
            placeholder="sensor.wallonia_electricity_price"
            .value=${t.price_entity??""}
            @input=${e=>this._set("price_entity",e.target.value||void 0)}
          />
        </label>

        <label class="field">
          <span>Static price fallback (€/kWh, optional)</span>
          <input
            type="number"
            step="0.0001"
            placeholder="0.3783"
            .value=${t.price!==void 0?String(t.price):""}
            @input=${e=>{let i=e.target.value;this._set("price",i===""?void 0:Number(i))}}
          />
        </label>

        <label class="field toggle">
          <span>Use Home Assistant Energy price</span>
          <input
            type="checkbox"
            .checked=${t.use_energy_prefs??!1}
            @change=${e=>this._set("use_energy_prefs",e.target.checked)}
          />
        </label>

        <label class="field">
          <span>Curve lookback (hours)</span>
          <input
            type="number"
            min="1"
            max="24"
            .value=${String(t.curve_hours??4)}
            @input=${e=>this._set("curve_hours",Number(e.target.value))}
          />
        </label>

        ${Ie.map(e=>f`
            <label class="field toggle">
              <span>${e.label}</span>
              <input
                type="checkbox"
                .checked=${t[e.key]??!0}
                @change=${i=>this._set(e.key,i.target.checked)}
              />
            </label>
          `)}
      </div>
    `}_renderDevicePicker(t){return customElements.get("ha-device-picker")&&this.hass?f`
        <ha-device-picker
          .hass=${this.hass}
          .value=${t.device??""}
          .label=${"Wellborne device"}
          .includeDomains=${["wellborne"]}
          @value-changed=${e=>this._set("device",e.detail.value||void 0)}
        ></ha-device-picker>
      `:f`
      <label class="field">
        <span>Wellborne device id</span>
        <input
          type="text"
          .value=${t.device??""}
          @input=${e=>this._set("device",e.target.value||void 0)}
        />
      </label>
    `}_set(t,e){if(!this._config)return;let i={...this._config};e===void 0||e===""?delete i[t]:i[t]=e,this._config=i,this.dispatchEvent(new CustomEvent("config-changed",{detail:{config:i},bubbles:!0,composed:!0}))}};P.styles=D`
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
  `,S([st({attribute:!1})],P.prototype,"hass",2),S([O()],P.prototype,"_config",2);customElements.get(Y)||customElements.define(Y,P)});L();$t();L();var te=D`
  :host {
    /* Theme-adaptive tokens with doc section-2 fallbacks. */
    --wb-surface: var(--ha-card-background, var(--card-background-color, #1c1c1e));
    --wb-primary: var(--primary-text-color, #e1e1e1);
    --wb-secondary: var(--secondary-text-color, #9b9b9b);
    --wb-divider: var(--divider-color, rgba(255, 255, 255, 0.12));
    --wb-accent: var(--wellborne-charging-color, #0f9d58);
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
    margin-top: 8px;
    background: var(--wb-chip-bg);
    border-radius: 12px;
    padding: 8px 12px;
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
`;Z();Z();function ne(n,t){let e={},i=Object.keys(ot);for(let r of i){let o=t[`${r}_entity`];typeof o=="string"&&o.length>0&&(e[r]=o)}if(!t.device)return e;let s=Pe(n,t.device);if(n.entities&&s){for(let r of Object.values(n.entities))if(r.device_id===t.device&&r.platform===rt&&r.unique_id)for(let o of i)e[o]||r.unique_id===`${s}_${ot[o]}`&&(e[o]=r.entity_id)}if(n.entities)for(let r of Object.values(n.entities))r.device_id===t.device&&se(e,i,r.entity_id,r.platform);if(!n.entities)for(let r of Object.keys(n.states))se(e,i,r);return e}function Pe(n,t){let e=n.devices?.[t];if(e){for(let i of e.identifiers)if(i[0]===rt)return i[1]}}function se(n,t,e,i){let s=e.indexOf(".");if(s<0)return;let r=e.slice(0,s),o=e.slice(s+1);for(let c of t){if(n[c])continue;let l=ie.has(c)?"binary_sensor":"sensor";if(r!==l||i&&i!==rt)continue;let u=ot[c];He(o,u)&&(n[c]=e)}}function He(n,t){if(!n.endsWith(`_${t}`))return!1;let e=n.slice(0,n.length-t.length-1);return!(t==="current"&&(e.endsWith("_max")||e.includes("household"))||t==="energy"&&e.endsWith("_last_session"))}Z();async function re(n,t){let e=Me(n,t.price_entity);if(e!==null)return{price:e,source:"CREG"};if(typeof t.price=="number"&&Number.isFinite(t.price)&&t.price>0)return{price:t.price,source:"static"};if(t.use_energy_prefs){let i=await Le(n);if(i!==null)return{price:i,source:"energy-prefs"}}return null}function Me(n,t){if(!t)return null;let e=n.states[t];if(!e||$.has(e.state))return null;let i=Number(e.state);if(!Number.isFinite(i))return null;let s=String(e.attributes.unit_of_measurement??"").toLowerCase();return Ne(i,s)}function Ne(n,t){let e=t.replace(/\s+/g,"");return e.includes("/mwh")?n/1e3:e.includes("/wh")&&!e.includes("/kwh")?n*1e3:n}async function Le(n){let t;try{t=await n.callWS({type:"energy/get_prefs"})}catch{return null}let i=t.energy_sources?.find(s=>s.type==="grid")?.flow_from?.[0];if(!i)return null;if(i.entity_energy_price){let s=n.states[i.entity_energy_price];if(s&&!$.has(s.state)){let r=Number(s.state);if(Number.isFinite(r))return r}}return typeof i.number_energy_price=="number"&&Number.isFinite(i.number_energy_price)?i.number_energy_price:null}function oe(n,t){return n===null||!Number.isFinite(n)?null:n*t}function wt(n,t,e){let i=t.currency??n.config.currency??"EUR";try{return new Intl.NumberFormat(n.locale.language,{style:"currency",currency:i}).format(e)}catch{return`${e.toFixed(2)} ${i}`}}L();function Oe(n,t,e,i=2){let s=n.filter(d=>Number.isFinite(d.v));if(s.length===0)return{line:"",area:"",tip:null};if(s.length===1){let d=e/2;return{line:`M ${i} ${d} L ${t-i} ${d}`,area:`M ${i} ${d} L ${t-i} ${d} L ${t-i} ${e} L ${i} ${e} Z`,tip:{x:t-i,y:d}}}let r=s[0].t,c=s[s.length-1].t-r||1,a=-1/0,l=1/0;for(let d of s)d.v>a&&(a=d.v),d.v<l&&(l=d.v);l=Math.min(l,0);let u=a-l||1,h=t-i*2,_=e-i*2,g=s.map(d=>{let ue=i+(d.t-r)/c*h,de=i+_-(d.v-l)/u*_;return{x:ue,y:de}}),x=`M ${E(g[0].x)} ${E(g[0].y)}`;for(let d=1;d<g.length;d++)x+=` L ${E(g[d].x)} ${E(g[d].y)}`;let Et=g[g.length-1],pe=g[0],he=`${x} L ${E(Et.x)} ${E(e)} L ${E(pe.x)} ${E(e)} Z`;return{line:x,area:he,tip:Et}}function E(n){return(Math.round(n*100)/100).toString()}function ae(n,t){let{width:e,height:i,gradientId:s,animate:r,live:o}=t,c=Oe(n,e,i);if(!c.line)return A`<svg viewBox="0 0 ${e} ${i}" width="100%" height="${i}" aria-hidden="true"></svg>`;let a=c.tip?A`
        <circle
          class="curve-tip ${o?"live":"static"} ${r?"animate":"noanim"}"
          cx="${c.tip.x}"
          cy="${c.tip.y}"
          r="2.6"
        ></circle>`:p;return A`
    <svg viewBox="0 0 ${e} ${i}" width="100%" height="${i}" preserveAspectRatio="none" aria-hidden="true">
      <defs>
        <linearGradient id="${s}" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="var(--wb-accent)" stop-opacity="0.18"></stop>
          <stop offset="100%" stop-color="var(--wb-accent)" stop-opacity="0"></stop>
        </linearGradient>
      </defs>
      <path class="curve-area" d="${c.area}" fill="url(#${s})"></path>
      <path class="curve-line" d="${c.line}" fill="none"></path>
      ${a}
    </svg>
  `}L();function ce(n){let t=n.size??96,e=8,i=(t-e)/2,s=t/2,r=t/2,o=2*Math.PI*i,c=Ue(n.percent,0,100),a=c/100*o,l=n.animate?"soc-arc animate":"soc-arc";return A`
    <svg viewBox="0 0 ${t} ${t}" width="${t}" height="${t}" class="soc-ring" role="img"
         aria-label="State of charge ${Math.round(c)} percent">
      <circle class="soc-track" cx="${s}" cy="${r}" r="${i}" fill="none" stroke-width="${e}"></circle>
      <circle
        class="${l}"
        cx="${s}"
        cy="${r}"
        r="${i}"
        fill="none"
        stroke-width="${e}"
        stroke-linecap="round"
        stroke-dasharray="${a} ${o-a}"
        transform="rotate(-90 ${s} ${r})"
      ></circle>
      <text class="soc-pct" x="${s}" y="${n.rangeLabel?r-2:r+1}" text-anchor="middle" dominant-baseline="middle">${Math.round(c)}%</text>
      ${n.rangeLabel?A`<text class="soc-range" x="${s}" y="${r+14}" text-anchor="middle" dominant-baseline="middle">${n.rangeLabel}</text>`:A``}
    </svg>
  `}function Ue(n,t,e){return Math.min(e,Math.max(t,n))}At();var De=220,ze=56,H=class extends v{constructor(){super(...arguments);this._history=[];this._price=null;this._entities={};this._lastHistoryFetch=0;this._historyKey="";this._priceKey=""}static async getConfigElement(){return await Promise.resolve().then(()=>(At(),le)),document.createElement(Y)}static getStubConfig(){return{type:`custom:${V}`,device:"",...xt}}getCardSize(){return 4}setConfig(e){if(!e)throw new Error("Invalid configuration");this._config={...xt,...e}}set hass(e){this._hass=e,this._config&&(this._entities=ne(e,this._config),this._maybeFetchHistory(),this._maybeResolvePrice(),this.requestUpdate())}get hass(){return this._hass}connectedCallback(){super.connectedCallback(),this._tick=setInterval(()=>{if(!this._hass||!this._config||this._cardState()!=="charging")return;typeof this._stateOf("session_duration")?.attributes?.duration_seconds=="number"&&this.requestUpdate()},1e3)}disconnectedCallback(){super.disconnectedCallback(),this._tick&&(clearInterval(this._tick),this._tick=void 0)}_maybeResolvePrice(){if(!this._hass||!this._config.show_cost)return;let e=`${this._config.price_entity??""}|${this._config.price??""}|${this._config.use_energy_prefs??""}|${this._priceEntityState()}`;e!==this._priceKey&&(this._priceKey=e,re(this._hass,this._config).then(i=>{this._price=i}).catch(()=>{this._price=null}))}_priceEntityState(){let e=this._config.price_entity;return!e||!this._hass?"":this._hass.states[e]?.state??""}_maybeFetchHistory(){if(!this._hass||!this._config.show_curve)return;let e=this._entities.power;if(!e)return;let i=Date.now();if(!(e!==this._historyKey)&&i-this._lastHistoryFetch<25e3)return;this._historyKey=e,this._lastHistoryFetch=i;let r=this._config.curve_hours??4,o=new Date(i-r*36e5).toISOString(),c=`history/period/${encodeURIComponent(o)}?filter_entity_id=${encodeURIComponent(e)}&minimal_response&no_attributes`;this._hass.callApi("GET",c).then(a=>{this._history=this._parseHistory(a,e)}).catch(()=>{this._history=[]})}_parseHistory(e,i){let s=Array.isArray(e)?e.find(o=>o[0]?.entity_id===i)??e[0]:void 0;if(!s)return[];let r=[];for(let o of s){let c=Number(o.state);if(!Number.isFinite(c))continue;let a=o.last_changed??o.last_updated;r.push({t:a?Date.parse(a):Date.now(),v:c})}return r}_stateOf(e){let i=this._entities[e];if(!(!i||!this._hass))return this._hass.states[i]}_num(e){let i=this._stateOf(e);if(!i||$.has(i.state))return null;let s=Number(i.state);return Number.isFinite(s)?s:null}_str(e){let i=this._stateOf(e);return!i||$.has(i.state)?null:i.state}_bool(e){let i=this._stateOf(e);return!i||$.has(i.state)?null:i.state==="on"}_cardState(){if(this._bool("charger_online")===!1)return"offline";let i=this._bool("charging"),s=this._str("status");return i===!0||s==="charging"?"charging":"idle"}render(){if(!this._config||!this._hass)return p;let e=this._cardState(),i=this._config.name??this._hass.devices?.[this._config.device??""]?.name??"Wellborne Charger";return f`
      <ha-card @click=${this._handleTap}>
        <div class="card ${e}">
          ${this._renderHeader(i,e)}
          ${this._renderHero(e)}
          ${this._config.show_curve?this._renderCurveBlock(e):p}
          ${this._renderChips(e)}
          ${this._renderFooter()}
        </div>
      </ha-card>
    `}_renderHeader(e,i){let s=i!=="offline",r=i==="charging"?f`<span class="badge charging"><ha-icon icon="mdi:lightning-bolt"></ha-icon>Charging</span>`:i==="offline"?f`<span class="badge offline"><ha-icon icon="mdi:cloud-off-outline"></ha-icon>Offline</span>`:f`<span class="badge"><ha-icon icon="mdi:sleep"></ha-icon>Idle</span>`;return f`
      <div class="header">
        <div class="title">${e}</div>
        <div class="header-right">
          ${r}
          <span class="dot ${s?"online":"offline"}" title=${s?"online":"offline"}></span>
        </div>
      </div>
    `}_renderHero(e){let i=e==="offline",s=this._num("power"),r=i||s===null?y:(s/1e3).toFixed(1),o=this._durationDisplay(e);return f`
      <div class="hero">
        ${this._renderRing(e)}
        <div class="hero-main">
          <div class="live-row">
            <div class="kw">${r}<span class="unit">${r===y?"":"kW"}</span></div>
            <div class="duration">${o}</div>
          </div>
        </div>
      </div>
    `}_renderRing(e){let i=this._config.battery_entity;if(!i||!this._hass)return p;let s=this._hass.states[i];if(!s||$.has(s.state))return p;let r=Number(s.state);if(!Number.isFinite(r))return p;let o=this._rangeLabel(e);return f`
      <div class="ring-wrap">
        ${ce({percent:r,rangeLabel:o,animate:!this._reducedMotion()})}
      </div>
    `}_rangeLabel(e){if(e==="offline")return;let i=this._config.range_entity;if(i&&this._hass){let r=this._hass.states[i];if(r&&!$.has(r.state)&&Number.isFinite(Number(r.state)))return`${Math.round(Number(r.state))} km`}let s=this._num("added_range");return s===null?void 0:`+${Math.round(s)} km`}_renderCurveBlock(e){let i=e==="charging";return f`
      <div class="curve ${e}">
        <span class="curve-label">${i?"Live power":"Last session"}</span>
        ${ae(this._history,{width:De,height:ze,gradientId:"wb-curve-grad",animate:!this._reducedMotion(),live:i})}
      </div>
    `}_chip(e,i,s=!1){return f`<span class="chip ${s?"on":""}"><ha-icon icon=${e}></ha-icon>${i}</span>`}_renderChips(e){let i=e==="offline",s=this._bool("vehicle_connected"),r=i?null:this._num("current"),o=i?null:this._num("max_current"),c=r===null?y:o===null?`${r.toFixed(0)} A`:`${r.toFixed(0)} / ${o.toFixed(0)} A`,a=i?null:this._num("energy"),l=i?null:this._num("added_range"),u=i?null:this._num("session_cost"),h=s===!0?this._chip("mdi:power-plug","Connected",!0):this._chip("mdi:power-plug-outline",y);return f`
      <div class="chips">
        ${h} ${this._chip("mdi:current-ac",c)}
        ${this._chip("mdi:lightning-bolt",a===null?y:`${a.toFixed(1)} kWh`)}
        ${this._chip("mdi:map-marker-distance",l===null?y:`+${Math.round(l)} km`)}
        ${u===null||this._hass===void 0?p:this._chip("mdi:cash",wt(this._hass,this._config,u))}
      </div>
    `}_renderFooter(){let e=this._config.show_totals,i=this._config.show_cost;return!e&&!i?p:f`
      <div class="footer">
        ${e?this._renderTotals():p}
        ${i?this._renderLastCharge():p}
      </div>
    `}_renderTotals(){let e=this._num("monthly_energy"),i=this._num("yearly_energy");return f`
      <div class="stats">
        <div class="stat">
          <span class="stat-label">This month</span>
          <span class="stat-value">${e===null?y:`${this._fmtKwh(e)}`}<span class="stat-unit">kWh</span></span>
        </div>
        <div class="stat">
          <span class="stat-label">This year</span>
          <span class="stat-value">${i===null?y:`${this._fmtKwh(i)}`}<span class="stat-unit">kWh</span></span>
        </div>
      </div>
    `}_renderLastCharge(){let e=this._num("last_session_energy"),i=this._num("last_session_duration"),r=`${e===null?y:`${this._fmtKwh(e)} kWh`} \xB7 ${this._formatDuration(i)}`,o=this._price===null?null:oe(e,this._price.price);if(o===null)return f`
        <div class="last">
          <div class="last-info">
            <span class="last-label"><ha-icon icon="mdi:history"></ha-icon>Last charge</span>
            <span class="last-detail">${r}</span>
          </div>
        </div>
      `;let c=wt(this._hass,this._config,o),a=this._price.source;return f`
      <div class="last">
        <div class="last-info">
          <span class="last-label"><ha-icon icon="mdi:history"></ha-icon>Last charge</span>
          <span class="last-detail">${r}</span>
        </div>
        <div class="last-cost">
          <span class="last-cost-value">~${c}</span>
          <span class="last-cost-caption">est. · ${a}</span>
        </div>
      </div>
    `}_formatDuration(e){if(e===null||!Number.isFinite(e)||e<0)return y;let i=Math.floor(e/60),s=Math.round(e%60);return`${i}:${s.toString().padStart(2,"0")}`}_durationDisplay(e){if(e==="offline")return y;let i=this._stateOf("session_duration"),s=i?.attributes?.duration_seconds;if(typeof s=="number"&&Number.isFinite(s)){let r=s;if(e==="charging"&&i?.last_updated){let o=(Date.now()-new Date(i.last_updated).getTime())/1e3;o>0&&o<15&&(r+=o)}return this._formatHMS(r)}return this._formatDuration(this._num("session_duration"))}_formatHMS(e){let i=Math.max(0,Math.floor(e)),s=Math.floor(i/3600),r=Math.floor(i%3600/60),o=i%60,c=r.toString().padStart(2,"0"),a=o.toString().padStart(2,"0");return s>0?`${s}:${c}:${a}`:`${r}:${a}`}_fmtKwh(e){return new Intl.NumberFormat(this._hass.locale.language,{maximumFractionDigits:1}).format(e)}_reducedMotion(){return typeof window<"u"&&typeof window.matchMedia=="function"&&window.matchMedia("(prefers-reduced-motion: reduce)").matches}_handleTap(){let e=this._entities.status??this._entities.power??this._entities.charger_online;e&&this.dispatchEvent(new CustomEvent("hass-more-info",{detail:{entityId:e},bubbles:!0,composed:!0}))}};H.styles=te,S([O()],H.prototype,"_config",2),S([O()],H.prototype,"_history",2),S([O()],H.prototype,"_price",2);customElements.get(V)||customElements.define(V,H);window.customCards=window.customCards??[];window.customCards.push({type:V,name:"Wellborne Charger Card",description:"Monitoring card for the Wellborne EV charger (live status, energy, cost).",preview:!0,documentationURL:"https://github.com/your/repo/tree/main/charger-card"});console.info(`%c WELLBORNE-CHARGER-CARD %c v${ee} `,"background:#0f9d58;color:#fff","");export{H as WellborneChargerCard};
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
