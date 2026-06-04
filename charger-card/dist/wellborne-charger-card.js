var Et=Object.defineProperty;var fe=Object.getOwnPropertyDescriptor;var m=(i,t)=>()=>(i&&(t=i(i=0)),t);var me=(i,t)=>{for(var e in t)Et(i,e,{get:t[e],enumerable:!0})};var S=(i,t,e,r)=>{for(var n=r>1?void 0:r?fe(t,e):t,s=i.length-1,o;s>=0;s--)(o=i[s])&&(n=(r?o(t,e,n):o(n))||n);return r&&n&&Et(t,e,n),n};var J,Q,at,St,I,Ct,D,kt,ct,lt=m(()=>{J=globalThis,Q=J.ShadowRoot&&(J.ShadyCSS===void 0||J.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,at=Symbol(),St=new WeakMap,I=class{constructor(t,e,r){if(this._$cssResult$=!0,r!==at)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t,this.t=e}get styleSheet(){let t=this.o,e=this.t;if(Q&&t===void 0){let r=e!==void 0&&e.length===1;r&&(t=St.get(e)),t===void 0&&((this.o=t=new CSSStyleSheet).replaceSync(this.cssText),r&&St.set(e,t))}return t}toString(){return this.cssText}},Ct=i=>new I(typeof i=="string"?i:i+"",void 0,at),D=(i,...t)=>{let e=i.length===1?i[0]:t.reduce((r,n,s)=>r+(o=>{if(o._$cssResult$===!0)return o.cssText;if(typeof o=="number")return o;throw Error("Value passed to 'css' function must be a 'css' function result: "+o+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(n)+i[s+1],i[0]);return new I(e,i,at)},kt=(i,t)=>{if(Q)i.adoptedStyleSheets=t.map(e=>e instanceof CSSStyleSheet?e:e.styleSheet);else for(let e of t){let r=document.createElement("style"),n=J.litNonce;n!==void 0&&r.setAttribute("nonce",n),r.textContent=e.cssText,i.appendChild(r)}},ct=Q?i=>i:i=>i instanceof CSSStyleSheet?(t=>{let e="";for(let r of t.cssRules)e+=r.cssText;return Ct(e)})(i):i});var ge,_e,ye,ve,be,$e,X,Rt,we,xe,F,W,tt,Tt,b,z=m(()=>{lt();lt();({is:ge,defineProperty:_e,getOwnPropertyDescriptor:ye,getOwnPropertyNames:ve,getOwnPropertySymbols:be,getPrototypeOf:$e}=Object),X=globalThis,Rt=X.trustedTypes,we=Rt?Rt.emptyScript:"",xe=X.reactiveElementPolyfillSupport,F=(i,t)=>i,W={toAttribute(i,t){switch(t){case Boolean:i=i?we:null;break;case Object:case Array:i=i==null?i:JSON.stringify(i)}return i},fromAttribute(i,t){let e=i;switch(t){case Boolean:e=i!==null;break;case Number:e=i===null?null:Number(i);break;case Object:case Array:try{e=JSON.parse(i)}catch{e=null}}return e}},tt=(i,t)=>!ge(i,t),Tt={attribute:!0,type:String,converter:W,reflect:!1,useDefault:!1,hasChanged:tt};Symbol.metadata??=Symbol("metadata"),X.litPropertyMetadata??=new WeakMap;b=class extends HTMLElement{static addInitializer(t){this._$Ei(),(this.l??=[]).push(t)}static get observedAttributes(){return this.finalize(),this._$Eh&&[...this._$Eh.keys()]}static createProperty(t,e=Tt){if(e.state&&(e.attribute=!1),this._$Ei(),this.prototype.hasOwnProperty(t)&&((e=Object.create(e)).wrapped=!0),this.elementProperties.set(t,e),!e.noAccessor){let r=Symbol(),n=this.getPropertyDescriptor(t,r,e);n!==void 0&&_e(this.prototype,t,n)}}static getPropertyDescriptor(t,e,r){let{get:n,set:s}=ye(this.prototype,t)??{get(){return this[e]},set(o){this[e]=o}};return{get:n,set(o){let a=n?.call(this);s?.call(this,o),this.requestUpdate(t,a,r)},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)??Tt}static _$Ei(){if(this.hasOwnProperty(F("elementProperties")))return;let t=$e(this);t.finalize(),t.l!==void 0&&(this.l=[...t.l]),this.elementProperties=new Map(t.elementProperties)}static finalize(){if(this.hasOwnProperty(F("finalized")))return;if(this.finalized=!0,this._$Ei(),this.hasOwnProperty(F("properties"))){let e=this.properties,r=[...ve(e),...be(e)];for(let n of r)this.createProperty(n,e[n])}let t=this[Symbol.metadata];if(t!==null){let e=litPropertyMetadata.get(t);if(e!==void 0)for(let[r,n]of e)this.elementProperties.set(r,n)}this._$Eh=new Map;for(let[e,r]of this.elementProperties){let n=this._$Eu(e,r);n!==void 0&&this._$Eh.set(n,e)}this.elementStyles=this.finalizeStyles(this.styles)}static finalizeStyles(t){let e=[];if(Array.isArray(t)){let r=new Set(t.flat(1/0).reverse());for(let n of r)e.unshift(ct(n))}else t!==void 0&&e.push(ct(t));return e}static _$Eu(t,e){let r=e.attribute;return r===!1?void 0:typeof r=="string"?r:typeof t=="string"?t.toLowerCase():void 0}constructor(){super(),this._$Ep=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Em=null,this._$Ev()}_$Ev(){this._$ES=new Promise(t=>this.enableUpdating=t),this._$AL=new Map,this._$E_(),this.requestUpdate(),this.constructor.l?.forEach(t=>t(this))}addController(t){(this._$EO??=new Set).add(t),this.renderRoot!==void 0&&this.isConnected&&t.hostConnected?.()}removeController(t){this._$EO?.delete(t)}_$E_(){let t=new Map,e=this.constructor.elementProperties;for(let r of e.keys())this.hasOwnProperty(r)&&(t.set(r,this[r]),delete this[r]);t.size>0&&(this._$Ep=t)}createRenderRoot(){let t=this.shadowRoot??this.attachShadow(this.constructor.shadowRootOptions);return kt(t,this.constructor.elementStyles),t}connectedCallback(){this.renderRoot??=this.createRenderRoot(),this.enableUpdating(!0),this._$EO?.forEach(t=>t.hostConnected?.())}enableUpdating(t){}disconnectedCallback(){this._$EO?.forEach(t=>t.hostDisconnected?.())}attributeChangedCallback(t,e,r){this._$AK(t,r)}_$ET(t,e){let r=this.constructor.elementProperties.get(t),n=this.constructor._$Eu(t,r);if(n!==void 0&&r.reflect===!0){let s=(r.converter?.toAttribute!==void 0?r.converter:W).toAttribute(e,r.type);this._$Em=t,s==null?this.removeAttribute(n):this.setAttribute(n,s),this._$Em=null}}_$AK(t,e){let r=this.constructor,n=r._$Eh.get(t);if(n!==void 0&&this._$Em!==n){let s=r.getPropertyOptions(n),o=typeof s.converter=="function"?{fromAttribute:s.converter}:s.converter?.fromAttribute!==void 0?s.converter:W;this._$Em=n;let a=o.fromAttribute(e,s.type);this[n]=a??this._$Ej?.get(n)??a,this._$Em=null}}requestUpdate(t,e,r,n=!1,s){if(t!==void 0){let o=this.constructor;if(n===!1&&(s=this[t]),r??=o.getPropertyOptions(t),!((r.hasChanged??tt)(s,e)||r.useDefault&&r.reflect&&s===this._$Ej?.get(t)&&!this.hasAttribute(o._$Eu(t,r))))return;this.C(t,e,r)}this.isUpdatePending===!1&&(this._$ES=this._$EP())}C(t,e,{useDefault:r,reflect:n,wrapped:s},o){r&&!(this._$Ej??=new Map).has(t)&&(this._$Ej.set(t,o??e??this[t]),s!==!0||o!==void 0)||(this._$AL.has(t)||(this.hasUpdated||r||(e=void 0),this._$AL.set(t,e)),n===!0&&this._$Em!==t&&(this._$Eq??=new Set).add(t))}async _$EP(){this.isUpdatePending=!0;try{await this._$ES}catch(e){Promise.reject(e)}let t=this.scheduleUpdate();return t!=null&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){if(!this.isUpdatePending)return;if(!this.hasUpdated){if(this.renderRoot??=this.createRenderRoot(),this._$Ep){for(let[n,s]of this._$Ep)this[n]=s;this._$Ep=void 0}let r=this.constructor.elementProperties;if(r.size>0)for(let[n,s]of r){let{wrapped:o}=s,a=this[n];o!==!0||this._$AL.has(n)||a===void 0||this.C(n,void 0,s,a)}}let t=!1,e=this._$AL;try{t=this.shouldUpdate(e),t?(this.willUpdate(e),this._$EO?.forEach(r=>r.hostUpdate?.()),this.update(e)):this._$EM()}catch(r){throw t=!1,this._$EM(),r}t&&this._$AE(e)}willUpdate(t){}_$AE(t){this._$EO?.forEach(e=>e.hostUpdated?.()),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t)}_$EM(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$ES}shouldUpdate(t){return!0}update(t){this._$Eq&&=this._$Eq.forEach(e=>this._$ET(e,this[e])),this._$EM()}updated(t){}firstUpdated(t){}};b.elementStyles=[],b.shadowRootOptions={mode:"open"},b[F("elementProperties")]=new Map,b[F("finalized")]=new Map,xe?.({ReactiveElement:b}),(X.reactiveElementVersions??=[]).push("2.1.2")});function Wt(i,t){if(!_t(i)||!i.hasOwnProperty("raw"))throw Error("invalid template strings array");return Mt!==void 0?Mt.createHTML(t):t}function H(i,t,e=i,r){if(t===T)return t;let n=r!==void 0?e._$Co?.[r]:e._$Cl,s=B(t)?void 0:t._$litDirective$;return n?.constructor!==s&&(n?._$AO?.(!1),s===void 0?n=void 0:(n=new s(i),n._$AT(i,e,r)),r!==void 0?(e._$Co??=[])[r]=n:e._$Cl=n),n!==void 0&&(t=H(i,n._$AS(i,t.values),n,r)),t}var gt,Pt,et,Mt,It,x,Dt,Ae,R,K,B,_t,Ee,ut,j,Ht,Nt,C,Ot,Lt,Ft,yt,d,A,qe,T,u,Ut,k,Se,q,pt,V,N,ht,dt,ft,mt,Ce,zt,rt=m(()=>{gt=globalThis,Pt=i=>i,et=gt.trustedTypes,Mt=et?et.createPolicy("lit-html",{createHTML:i=>i}):void 0,It="$lit$",x=`lit$${Math.random().toFixed(9).slice(2)}$`,Dt="?"+x,Ae=`<${Dt}>`,R=document,K=()=>R.createComment(""),B=i=>i===null||typeof i!="object"&&typeof i!="function",_t=Array.isArray,Ee=i=>_t(i)||typeof i?.[Symbol.iterator]=="function",ut=`[ 	
\f\r]`,j=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,Ht=/-->/g,Nt=/>/g,C=RegExp(`>|${ut}(?:([^\\s"'>=/]+)(${ut}*=${ut}*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`,"g"),Ot=/'/g,Lt=/"/g,Ft=/^(?:script|style|textarea|title)$/i,yt=i=>(t,...e)=>({_$litType$:i,strings:t,values:e}),d=yt(1),A=yt(2),qe=yt(3),T=Symbol.for("lit-noChange"),u=Symbol.for("lit-nothing"),Ut=new WeakMap,k=R.createTreeWalker(R,129);Se=(i,t)=>{let e=i.length-1,r=[],n,s=t===2?"<svg>":t===3?"<math>":"",o=j;for(let a=0;a<e;a++){let c=i[a],l,h,p=-1,y=0;for(;y<c.length&&(o.lastIndex=y,h=o.exec(c),h!==null);)y=o.lastIndex,o===j?h[1]==="!--"?o=Ht:h[1]!==void 0?o=Nt:h[2]!==void 0?(Ft.test(h[2])&&(n=RegExp("</"+h[2],"g")),o=C):h[3]!==void 0&&(o=C):o===C?h[0]===">"?(o=n??j,p=-1):h[1]===void 0?p=-2:(p=o.lastIndex-h[2].length,l=h[1],o=h[3]===void 0?C:h[3]==='"'?Lt:Ot):o===Lt||o===Ot?o=C:o===Ht||o===Nt?o=j:(o=C,n=void 0);let g=o===C&&i[a+1].startsWith("/>")?" ":"";s+=o===j?c+Ae:p>=0?(r.push(l),c.slice(0,p)+It+c.slice(p)+x+g):c+x+(p===-2?a:g)}return[Wt(i,s+(i[e]||"<?>")+(t===2?"</svg>":t===3?"</math>":"")),r]},q=class i{constructor({strings:t,_$litType$:e},r){let n;this.parts=[];let s=0,o=0,a=t.length-1,c=this.parts,[l,h]=Se(t,e);if(this.el=i.createElement(l,r),k.currentNode=this.el.content,e===2||e===3){let p=this.el.content.firstChild;p.replaceWith(...p.childNodes)}for(;(n=k.nextNode())!==null&&c.length<a;){if(n.nodeType===1){if(n.hasAttributes())for(let p of n.getAttributeNames())if(p.endsWith(It)){let y=h[o++],g=n.getAttribute(p).split(x),w=/([.?@])?(.*)/.exec(y);c.push({type:1,index:s,name:w[2],strings:g,ctor:w[1]==="."?ht:w[1]==="?"?dt:w[1]==="@"?ft:N}),n.removeAttribute(p)}else p.startsWith(x)&&(c.push({type:6,index:s}),n.removeAttribute(p));if(Ft.test(n.tagName)){let p=n.textContent.split(x),y=p.length-1;if(y>0){n.textContent=et?et.emptyScript:"";for(let g=0;g<y;g++)n.append(p[g],K()),k.nextNode(),c.push({type:2,index:++s});n.append(p[y],K())}}}else if(n.nodeType===8)if(n.data===Dt)c.push({type:2,index:s});else{let p=-1;for(;(p=n.data.indexOf(x,p+1))!==-1;)c.push({type:7,index:s}),p+=x.length-1}s++}}static createElement(t,e){let r=R.createElement("template");return r.innerHTML=t,r}};pt=class{constructor(t,e){this._$AV=[],this._$AN=void 0,this._$AD=t,this._$AM=e}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(t){let{el:{content:e},parts:r}=this._$AD,n=(t?.creationScope??R).importNode(e,!0);k.currentNode=n;let s=k.nextNode(),o=0,a=0,c=r[0];for(;c!==void 0;){if(o===c.index){let l;c.type===2?l=new V(s,s.nextSibling,this,t):c.type===1?l=new c.ctor(s,c.name,c.strings,this,t):c.type===6&&(l=new mt(s,this,t)),this._$AV.push(l),c=r[++a]}o!==c?.index&&(s=k.nextNode(),o++)}return k.currentNode=R,n}p(t){let e=0;for(let r of this._$AV)r!==void 0&&(r.strings!==void 0?(r._$AI(t,r,e),e+=r.strings.length-2):r._$AI(t[e])),e++}},V=class i{get _$AU(){return this._$AM?._$AU??this._$Cv}constructor(t,e,r,n){this.type=2,this._$AH=u,this._$AN=void 0,this._$AA=t,this._$AB=e,this._$AM=r,this.options=n,this._$Cv=n?.isConnected??!0}get parentNode(){let t=this._$AA.parentNode,e=this._$AM;return e!==void 0&&t?.nodeType===11&&(t=e.parentNode),t}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(t,e=this){t=H(this,t,e),B(t)?t===u||t==null||t===""?(this._$AH!==u&&this._$AR(),this._$AH=u):t!==this._$AH&&t!==T&&this._(t):t._$litType$!==void 0?this.$(t):t.nodeType!==void 0?this.T(t):Ee(t)?this.k(t):this._(t)}O(t){return this._$AA.parentNode.insertBefore(t,this._$AB)}T(t){this._$AH!==t&&(this._$AR(),this._$AH=this.O(t))}_(t){this._$AH!==u&&B(this._$AH)?this._$AA.nextSibling.data=t:this.T(R.createTextNode(t)),this._$AH=t}$(t){let{values:e,_$litType$:r}=t,n=typeof r=="number"?this._$AC(t):(r.el===void 0&&(r.el=q.createElement(Wt(r.h,r.h[0]),this.options)),r);if(this._$AH?._$AD===n)this._$AH.p(e);else{let s=new pt(n,this),o=s.u(this.options);s.p(e),this.T(o),this._$AH=s}}_$AC(t){let e=Ut.get(t.strings);return e===void 0&&Ut.set(t.strings,e=new q(t)),e}k(t){_t(this._$AH)||(this._$AH=[],this._$AR());let e=this._$AH,r,n=0;for(let s of t)n===e.length?e.push(r=new i(this.O(K()),this.O(K()),this,this.options)):r=e[n],r._$AI(s),n++;n<e.length&&(this._$AR(r&&r._$AB.nextSibling,n),e.length=n)}_$AR(t=this._$AA.nextSibling,e){for(this._$AP?.(!1,!0,e);t!==this._$AB;){let r=Pt(t).nextSibling;Pt(t).remove(),t=r}}setConnected(t){this._$AM===void 0&&(this._$Cv=t,this._$AP?.(t))}},N=class{get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}constructor(t,e,r,n,s){this.type=1,this._$AH=u,this._$AN=void 0,this.element=t,this.name=e,this._$AM=n,this.options=s,r.length>2||r[0]!==""||r[1]!==""?(this._$AH=Array(r.length-1).fill(new String),this.strings=r):this._$AH=u}_$AI(t,e=this,r,n){let s=this.strings,o=!1;if(s===void 0)t=H(this,t,e,0),o=!B(t)||t!==this._$AH&&t!==T,o&&(this._$AH=t);else{let a=t,c,l;for(t=s[0],c=0;c<s.length-1;c++)l=H(this,a[r+c],e,c),l===T&&(l=this._$AH[c]),o||=!B(l)||l!==this._$AH[c],l===u?t=u:t!==u&&(t+=(l??"")+s[c+1]),this._$AH[c]=l}o&&!n&&this.j(t)}j(t){t===u?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,t??"")}},ht=class extends N{constructor(){super(...arguments),this.type=3}j(t){this.element[this.name]=t===u?void 0:t}},dt=class extends N{constructor(){super(...arguments),this.type=4}j(t){this.element.toggleAttribute(this.name,!!t&&t!==u)}},ft=class extends N{constructor(t,e,r,n,s){super(t,e,r,n,s),this.type=5}_$AI(t,e=this){if((t=H(this,t,e,0)??u)===T)return;let r=this._$AH,n=t===u&&r!==u||t.capture!==r.capture||t.once!==r.once||t.passive!==r.passive,s=t!==u&&(r===u||n);n&&this.element.removeEventListener(this.name,this,r),s&&this.element.addEventListener(this.name,this,t),this._$AH=t}handleEvent(t){typeof this._$AH=="function"?this._$AH.call(this.options?.host??this.element,t):this._$AH.handleEvent(t)}},mt=class{constructor(t,e,r){this.element=t,this.type=6,this._$AN=void 0,this._$AM=e,this.options=r}get _$AU(){return this._$AM._$AU}_$AI(t){H(this,t)}},Ce=gt.litHtmlPolyfillSupport;Ce?.(q,V),(gt.litHtmlVersions??=[]).push("3.3.3");zt=(i,t,e)=>{let r=e?.renderBefore??t,n=r._$litPart$;if(n===void 0){let s=e?.renderBefore??null;r._$litPart$=n=new V(t.insertBefore(K(),s),s,void 0,e??{})}return n._$AI(i),n}});var vt,v,ke,jt=m(()=>{z();z();rt();rt();vt=globalThis,v=class extends b{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){let t=super.createRenderRoot();return this.renderOptions.renderBefore??=t.firstChild,t}update(t){let e=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Do=zt(e,this.renderRoot,this.renderOptions)}connectedCallback(){super.connectedCallback(),this._$Do?.setConnected(!0)}disconnectedCallback(){super.disconnectedCallback(),this._$Do?.setConnected(!1)}render(){return T}};v._$litElement$=!0,v.finalized=!0,vt.litElementHydrateSupport?.({LitElement:v});ke=vt.litElementPolyfillSupport;ke?.({LitElement:v});(vt.litElementVersions??=[]).push("4.2.2")});var Kt=m(()=>{});var O=m(()=>{z();rt();jt();Kt()});var Bt=m(()=>{});function nt(i){return(t,e)=>typeof e=="object"?Te(i,t,e):((r,n,s)=>{let o=n.hasOwnProperty(s);return n.constructor.createProperty(s,r),o?Object.getOwnPropertyDescriptor(n,s):void 0})(i,t,e)}var Re,Te,bt=m(()=>{z();Re={attribute:!0,type:String,converter:W,reflect:!1,hasChanged:tt},Te=(i=Re,t,e)=>{let{kind:r,metadata:n}=e,s=globalThis.litPropertyMetadata.get(n);if(s===void 0&&globalThis.litPropertyMetadata.set(n,s=new Map),r==="setter"&&((i=Object.create(i)).wrapped=!0),s.set(e.name,i),r==="accessor"){let{name:o}=e;return{set(a){let c=t.get.call(this);t.set.call(this,a),this.requestUpdate(o,c,i,!0,a)},init(a){return a!==void 0&&this.C(o,void 0,i,a),a}}}if(r==="setter"){let{name:o}=e;return function(a){let c=this[o];t.call(this,a),this.requestUpdate(o,c,i,!0,a)}}throw Error("Unsupported decorator location: "+r)}});function L(i){return nt({...i,state:!0,attribute:!1})}var qt=m(()=>{bt();});var Vt=m(()=>{});var U=m(()=>{});var Gt=m(()=>{U();});var Yt=m(()=>{U();});var Zt=m(()=>{U();});var Jt=m(()=>{U();});var Qt=m(()=>{U();});var $t=m(()=>{Bt();bt();qt();Vt();Gt();Yt();Zt();Jt();Qt()});var G,Y,te,st,ot,ee,$,_,wt,Z=m(()=>{"use strict";G="wellborne-charger-card",Y="wellborne-charger-card-editor",te="1.0.0",st="wellborne",ot={power:"power",energy:"energy",current:"current",max_current:"max_current",session_duration:"session_duration",status:"status",added_range:"added_range",monthly_energy:"monthly_energy",yearly_energy:"yearly_energy",last_session_energy:"last_session_energy",last_session_duration:"last_session_duration",session_cost:"session_cost",wifi_ssid:"wifi_ssid",charging:"charging",charger_online:"charger_online",vehicle_connected:"vehicle_connected"},ee=new Set(["charging","charger_online","vehicle_connected"]),$=new Set(["unavailable","unknown","none",""]),_="\u2014",wt={show_curve:!0,show_totals:!0,show_cost:!0,curve_hours:4}});var le={};me(le,{WellborneChargerCardEditor:()=>P});var Ie,P,xt=m(()=>{"use strict";O();$t();Z();Ie=[{key:"show_curve",label:"Power curve (sparkline)"},{key:"show_totals",label:"Month / year totals"},{key:"show_cost",label:"Last-charge cost"}],P=class extends v{setConfig(t){this._config=t}render(){if(!this._config)return u;let t=this._config;return d`
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
            @input=${e=>{let r=e.target.value;this._set("price",r===""?void 0:Number(r))}}
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

        ${Ie.map(e=>d`
            <label class="field toggle">
              <span>${e.label}</span>
              <input
                type="checkbox"
                .checked=${t[e.key]??!0}
                @change=${r=>this._set(e.key,r.target.checked)}
              />
            </label>
          `)}
      </div>
    `}_renderDevicePicker(t){return customElements.get("ha-device-picker")&&this.hass?d`
        <ha-device-picker
          .hass=${this.hass}
          .value=${t.device??""}
          .label=${"Wellborne device"}
          .includeDomains=${["wellborne"]}
          @value-changed=${e=>this._set("device",e.detail.value||void 0)}
        ></ha-device-picker>
      `:d`
      <label class="field">
        <span>Wellborne device id</span>
        <input
          type="text"
          .value=${t.device??""}
          @input=${e=>this._set("device",e.target.value||void 0)}
        />
      </label>
    `}_set(t,e){if(!this._config)return;let r={...this._config};e===void 0||e===""?delete r[t]:r[t]=e,this._config=r,this.dispatchEvent(new CustomEvent("config-changed",{detail:{config:r},bubbles:!0,composed:!0}))}};P.styles=D`
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
  `,S([nt({attribute:!1})],P.prototype,"hass",2),S([L()],P.prototype,"_config",2);customElements.get(Y)||customElements.define(Y,P)});O();$t();O();var Xt=D`
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
  /* Mirror the stat tiles: uppercase label (+ date) on top, bold value row below. */
  .last {
    display: flex;
    flex-direction: column;
    gap: 2px;
    margin-top: 8px;
    background: var(--wb-chip-bg);
    border-radius: 12px;
    padding: 8px 12px;
  }
  .last-head {
    display: flex;
    align-items: baseline;
    gap: 6px;
  }
  .last-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--wb-secondary);
  }
  .last-when {
    font-size: 0.72rem;
    color: var(--wb-secondary);
    opacity: 0.85;
    font-variant-numeric: tabular-nums;
  }
  .last-when::before {
    content: '·';
    margin-right: 6px;
    opacity: 0.6;
  }
  /* Value row matches .stat-value / .stat-unit exactly for cross-tile consistency. */
  .last-detail {
    font-size: 1.15rem;
    font-weight: 700;
    line-height: 1.1;
    color: var(--wb-primary);
    font-variant-numeric: tabular-nums;
  }
  .last-detail .metric {
    white-space: nowrap;
  }
  .last-detail .unit {
    font-size: 0.72rem;
    font-weight: 500;
    color: var(--wb-secondary);
    margin-left: 4px;
  }
  .last-detail .sep {
    margin: 0 6px;
    font-weight: 500;
    color: var(--wb-secondary);
    opacity: 0.55;
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
`;Z();Z();function ne(i,t){let e={},r=Object.keys(ot);for(let s of r){let o=t[`${s}_entity`];typeof o=="string"&&o.length>0&&(e[s]=o)}if(!t.device)return e;let n=Pe(i,t.device);if(i.entities&&n){for(let s of Object.values(i.entities))if(s.device_id===t.device&&s.platform===st&&s.unique_id)for(let o of r)e[o]||s.unique_id===`${n}_${ot[o]}`&&(e[o]=s.entity_id)}if(i.entities)for(let s of Object.values(i.entities))s.device_id===t.device&&re(e,r,s.entity_id,s.platform);if(!i.entities)for(let s of Object.keys(i.states))re(e,r,s);return e}function Pe(i,t){let e=i.devices?.[t];if(e){for(let r of e.identifiers)if(r[0]===st)return r[1]}}function re(i,t,e,r){let n=e.indexOf(".");if(n<0)return;let s=e.slice(0,n),o=e.slice(n+1);for(let a of t){if(i[a])continue;let l=ee.has(a)?"binary_sensor":"sensor";if(s!==l||r&&r!==st)continue;let h=ot[a];Me(o,h)&&(i[a]=e)}}function Me(i,t){if(!i.endsWith(`_${t}`))return!1;let e=i.slice(0,i.length-t.length-1);return!(t==="current"&&(e.endsWith("_max")||e.includes("household"))||t==="energy"&&e.endsWith("_last_session"))}Z();async function ie(i,t){let e=He(i,t.price_entity);if(e!==null)return{price:e,source:"CREG"};if(typeof t.price=="number"&&Number.isFinite(t.price)&&t.price>0)return{price:t.price,source:"static"};if(t.use_energy_prefs){let r=await Oe(i);if(r!==null)return{price:r,source:"energy-prefs"}}return null}function He(i,t){if(!t)return null;let e=i.states[t];if(!e||$.has(e.state))return null;let r=Number(e.state);if(!Number.isFinite(r))return null;let n=String(e.attributes.unit_of_measurement??"").toLowerCase();return Ne(r,n)}function Ne(i,t){let e=t.replace(/\s+/g,"");return e.includes("/mwh")?i/1e3:e.includes("/wh")&&!e.includes("/kwh")?i*1e3:i}async function Oe(i){let t;try{t=await i.callWS({type:"energy/get_prefs"})}catch{return null}let r=t.energy_sources?.find(n=>n.type==="grid")?.flow_from?.[0];if(!r)return null;if(r.entity_energy_price){let n=i.states[r.entity_energy_price];if(n&&!$.has(n.state)){let s=Number(n.state);if(Number.isFinite(s))return s}}return typeof r.number_energy_price=="number"&&Number.isFinite(r.number_energy_price)?r.number_energy_price:null}function se(i,t){return i===null||!Number.isFinite(i)?null:i*t}function oe(i,t,e){let r=t.currency??i.config.currency??"EUR";try{return new Intl.NumberFormat(i.locale.language,{style:"currency",currency:r}).format(e)}catch{return`${e.toFixed(2)} ${r}`}}O();function Le(i,t,e,r=2){let n=i.filter(f=>Number.isFinite(f.v));if(n.length===0)return{line:"",area:"",tip:null};if(n.length===1){let f=e/2;return{line:`M ${r} ${f} L ${t-r} ${f}`,area:`M ${r} ${f} L ${t-r} ${f} L ${t-r} ${e} L ${r} ${e} Z`,tip:{x:t-r,y:f}}}let s=n[0].t,a=n[n.length-1].t-s||1,c=-1/0,l=1/0;for(let f of n)f.v>c&&(c=f.v),f.v<l&&(l=f.v);l=Math.min(l,0);let h=c-l||1,p=t-r*2,y=e-r*2,g=n.map(f=>{let he=r+(f.t-s)/a*p,de=r+y-(f.v-l)/h*y;return{x:he,y:de}}),w=`M ${E(g[0].x)} ${E(g[0].y)}`;for(let f=1;f<g.length;f++)w+=` L ${E(g[f].x)} ${E(g[f].y)}`;let At=g[g.length-1],ue=g[0],pe=`${w} L ${E(At.x)} ${E(e)} L ${E(ue.x)} ${E(e)} Z`;return{line:w,area:pe,tip:At}}function E(i){return(Math.round(i*100)/100).toString()}function ae(i,t){let{width:e,height:r,gradientId:n,animate:s,live:o}=t,a=Le(i,e,r);if(!a.line)return A`<svg viewBox="0 0 ${e} ${r}" width="100%" height="${r}" aria-hidden="true"></svg>`;let c=a.tip?A`
        <circle
          class="curve-tip ${o?"live":"static"} ${s?"animate":"noanim"}"
          cx="${a.tip.x}"
          cy="${a.tip.y}"
          r="2.6"
        ></circle>`:u;return A`
    <svg viewBox="0 0 ${e} ${r}" width="100%" height="${r}" preserveAspectRatio="none" aria-hidden="true">
      <defs>
        <linearGradient id="${n}" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="var(--wb-accent)" stop-opacity="0.18"></stop>
          <stop offset="100%" stop-color="var(--wb-accent)" stop-opacity="0"></stop>
        </linearGradient>
      </defs>
      <path class="curve-area" d="${a.area}" fill="url(#${n})"></path>
      <path class="curve-line" d="${a.line}" fill="none"></path>
      ${c}
    </svg>
  `}O();function ce(i){let t=i.size??96,e=8,r=(t-e)/2,n=t/2,s=t/2,o=2*Math.PI*r,a=Ue(i.percent,0,100),c=a/100*o,l=i.animate?"soc-arc animate":"soc-arc";return A`
    <svg viewBox="0 0 ${t} ${t}" width="${t}" height="${t}" class="soc-ring" role="img"
         aria-label="State of charge ${Math.round(a)} percent">
      <circle class="soc-track" cx="${n}" cy="${s}" r="${r}" fill="none" stroke-width="${e}"></circle>
      <circle
        class="${l}"
        cx="${n}"
        cy="${s}"
        r="${r}"
        fill="none"
        stroke-width="${e}"
        stroke-linecap="round"
        stroke-dasharray="${c} ${o-c}"
        transform="rotate(-90 ${n} ${s})"
      ></circle>
      <text class="soc-pct" x="${n}" y="${i.rangeLabel?s-2:s+1}" text-anchor="middle" dominant-baseline="middle">${Math.round(a)}%</text>
      ${i.rangeLabel?A`<text class="soc-range" x="${n}" y="${s+14}" text-anchor="middle" dominant-baseline="middle">${i.rangeLabel}</text>`:A``}
    </svg>
  `}function Ue(i,t,e){return Math.min(e,Math.max(t,i))}xt();var De=220,Fe=56,M=class extends v{constructor(){super(...arguments);this._history=[];this._price=null;this._entities={};this._lastHistoryFetch=0;this._historyKey="";this._priceKey=""}static async getConfigElement(){return await Promise.resolve().then(()=>(xt(),le)),document.createElement(Y)}static getStubConfig(){return{type:`custom:${G}`,device:"",...wt}}getCardSize(){return 4}setConfig(e){if(!e)throw new Error("Invalid configuration");this._config={...wt,...e}}set hass(e){this._hass=e,this._config&&(this._entities=ne(e,this._config),this._maybeFetchHistory(),this._maybeResolvePrice(),this.requestUpdate())}get hass(){return this._hass}connectedCallback(){super.connectedCallback(),this._tick=setInterval(()=>{if(!this._hass||!this._config||this._cardState()!=="charging")return;typeof this._stateOf("session_duration")?.attributes?.duration_seconds=="number"&&this.requestUpdate()},1e3)}disconnectedCallback(){super.disconnectedCallback(),this._tick&&(clearInterval(this._tick),this._tick=void 0)}_maybeResolvePrice(){if(!this._hass||!this._config.show_cost)return;let e=`${this._config.price_entity??""}|${this._config.price??""}|${this._config.use_energy_prefs??""}|${this._priceEntityState()}`;e!==this._priceKey&&(this._priceKey=e,ie(this._hass,this._config).then(r=>{this._price=r}).catch(()=>{this._price=null}))}_priceEntityState(){let e=this._config.price_entity;return!e||!this._hass?"":this._hass.states[e]?.state??""}_maybeFetchHistory(){if(!this._hass||!this._config.show_curve)return;let e=this._entities.power;if(!e)return;let r=Date.now();if(!(e!==this._historyKey)&&r-this._lastHistoryFetch<25e3)return;this._historyKey=e,this._lastHistoryFetch=r;let s=this._config.curve_hours??4,o=new Date(r-s*36e5).toISOString(),a=`history/period/${encodeURIComponent(o)}?filter_entity_id=${encodeURIComponent(e)}&minimal_response&no_attributes`;this._hass.callApi("GET",a).then(c=>{this._history=this._parseHistory(c,e)}).catch(()=>{this._history=[]})}_parseHistory(e,r){let n=Array.isArray(e)?e.find(o=>o[0]?.entity_id===r)??e[0]:void 0;if(!n)return[];let s=[];for(let o of n){let a=Number(o.state);if(!Number.isFinite(a))continue;let c=o.last_changed??o.last_updated;s.push({t:c?Date.parse(c):Date.now(),v:a})}return s}_stateOf(e){let r=this._entities[e];if(!(!r||!this._hass))return this._hass.states[r]}_num(e){let r=this._stateOf(e);if(!r||$.has(r.state))return null;let n=Number(r.state);return Number.isFinite(n)?n:null}_str(e){let r=this._stateOf(e);return!r||$.has(r.state)?null:r.state}_bool(e){let r=this._stateOf(e);return!r||$.has(r.state)?null:r.state==="on"}_cardState(){if(this._bool("charger_online")===!1)return"offline";let r=this._bool("charging"),n=this._str("status");return r===!0||n==="charging"?"charging":"idle"}render(){if(!this._config||!this._hass)return u;let e=this._cardState(),r=this._config.name??this._hass.devices?.[this._config.device??""]?.name??"Wellborne Charger";return d`
      <ha-card @click=${this._handleTap}>
        <div class="card ${e}">
          ${this._renderHeader(r,e)}
          ${this._renderHero(e)}
          ${this._config.show_curve?this._renderCurveBlock(e):u}
          ${this._renderChips(e)}
          ${this._renderFooter()}
        </div>
      </ha-card>
    `}_renderHeader(e,r){let n=r!=="offline",s=r==="charging"?d`<span class="badge charging"><ha-icon icon="mdi:lightning-bolt"></ha-icon>Charging</span>`:r==="offline"?d`<span class="badge offline"><ha-icon icon="mdi:cloud-off-outline"></ha-icon>Offline</span>`:d`<span class="badge"><ha-icon icon="mdi:sleep"></ha-icon>Idle</span>`;return d`
      <div class="header">
        <div class="title">${e}</div>
        <div class="header-right">
          ${s}
          <span class="dot ${n?"online":"offline"}" title=${n?"online":"offline"}></span>
        </div>
      </div>
    `}_renderHero(e){let r=e==="offline",n=this._num("power"),s=r||n===null?_:(n/1e3).toFixed(1),o=this._durationDisplay(e);return d`
      <div class="hero">
        ${this._renderRing(e)}
        <div class="hero-main">
          <div class="live-row">
            <div class="kw">${s}<span class="unit">${s===_?"":"kW"}</span></div>
            <div class="duration">${o}</div>
          </div>
        </div>
      </div>
    `}_renderRing(e){let r=this._config.battery_entity;if(!r||!this._hass)return u;let n=this._hass.states[r];if(!n||$.has(n.state))return u;let s=Number(n.state);if(!Number.isFinite(s))return u;let o=this._rangeLabel(e);return d`
      <div class="ring-wrap">
        ${ce({percent:s,rangeLabel:o,animate:!this._reducedMotion()})}
      </div>
    `}_rangeLabel(e){if(e==="offline")return;let r=this._config.range_entity;if(r&&this._hass){let s=this._hass.states[r];if(s&&!$.has(s.state)&&Number.isFinite(Number(s.state)))return`${Math.round(Number(s.state))} km`}let n=this._num("added_range");return n===null?void 0:`+${Math.round(n)} km`}_renderCurveBlock(e){let r=e==="charging";return d`
      <div class="curve ${e}">
        <span class="curve-label">${r?"Live power":"Last session"}</span>
        ${ae(this._history,{width:De,height:Fe,gradientId:"wb-curve-grad",animate:!this._reducedMotion(),live:r})}
      </div>
    `}_chip(e,r,n=!1){return d`<span class="chip ${n?"on":""}"><ha-icon icon=${e}></ha-icon>${r}</span>`}_renderChips(e){let r=e==="offline",n=this._bool("vehicle_connected"),s=r?null:this._num("current"),o=r?null:this._num("max_current"),a=s===null?_:o===null?`${s.toFixed(0)} A`:`${s.toFixed(0)} / ${o.toFixed(0)} A`,c=r?null:this._num("energy"),l=r?null:this._num("added_range"),h=r?null:this._num("session_cost"),p=n===!0?this._chip("mdi:power-plug","Connected",!0):this._chip("mdi:power-plug-outline",_);return d`
      <div class="chips">
        ${p} ${this._chip("mdi:current-ac",a)}
        ${this._chip("mdi:lightning-bolt",c===null?_:`${c.toFixed(1)} kWh`)}
        ${this._chip("mdi:map-marker-distance",l===null?_:`+${Math.round(l)} km`)}
        ${h===null||this._hass===void 0?u:this._chip("mdi:cash",oe(this._hass,this._config,h))}
      </div>
    `}_renderFooter(){let e=this._config.show_totals,r=this._config.show_cost;return!e&&!r?u:d`
      <div class="footer">
        ${e?this._renderTotals():u}
        ${r?this._renderLastCharge():u}
      </div>
    `}_renderTotals(){let e=this._num("monthly_energy"),r=this._num("yearly_energy");return d`
      <div class="stats">
        <div class="stat">
          <span class="stat-label">This month</span>
          <span class="stat-value">${e===null?_:`${this._fmtKwh(e)}`}<span class="stat-unit">kWh</span></span>
        </div>
        <div class="stat">
          <span class="stat-label">This year</span>
          <span class="stat-value">${r===null?_:`${this._fmtKwh(r)}`}<span class="stat-unit">kWh</span></span>
        </div>
      </div>
    `}_renderLastCharge(){let e=this._num("last_session_energy"),r=this._num("last_session_duration"),n=this._stateOf("last_session_energy")?.attributes,s=typeof n?.added_range=="number"?n.added_range:null,o=this._formatWhen(n?.end_time),a=this._durationParts(r),c=[this._metric(e===null?_:this._fmtKwh(e),e===null?"":"kWh"),this._metric(a.value,a.unit)];s!==null&&Number.isFinite(s)&&c.push(this._metric(`+${Math.round(s)}`,"km"));let l=this._price===null?null:se(e,this._price.price);if(l!==null){let h=this._costParts(l);c.push(this._metric(h.value,h.unit))}return d`
      <div class="last">
        <div class="last-head">
          <span class="last-label">Last charge</span>
          ${o===null?u:d`<span class="last-when">${o}</span>`}
        </div>
        <div class="last-detail">
          ${c.map((h,p)=>d`${p>0?d`<span class="sep">·</span>`:u}${h}`)}
        </div>
      </div>
    `}_metric(e,r){return d`<span class="metric"
      >${e}${r===""?u:d`<span class="unit">${r}</span>`}</span
    >`}_durationParts(e){if(e===null||!Number.isFinite(e)||e<0)return{value:_,unit:""};if(e<60)return{value:String(Math.round(e)),unit:"min"};let r=Math.floor(e/60),n=Math.round(e%60);return{value:`${r}:${n.toString().padStart(2,"0")}`,unit:"h"}}_costParts(e){let r=this._config.currency??this._hass.config.currency??"EUR";try{let n=new Intl.NumberFormat(this._hass.locale.language,{style:"currency",currency:r,currencyDisplay:"narrowSymbol"}).formatToParts(e),s=n.find(a=>a.type==="currency")?.value??r;return{value:n.filter(a=>a.type!=="currency"&&a.type!=="literal").map(a=>a.value).join(""),unit:s}}catch{return{value:e.toFixed(2),unit:"\u20AC"}}}_formatWhen(e){if(typeof e!="string"||e==="")return null;let r=new Date(e);return Number.isNaN(r.getTime())?null:new Intl.DateTimeFormat(this._hass.locale.language,{month:"short",day:"numeric",hour:"2-digit",minute:"2-digit",hour12:!1}).format(r)}_formatDuration(e){if(e===null||!Number.isFinite(e)||e<0)return _;let r=Math.floor(e/60),n=Math.round(e%60);return`${r}:${n.toString().padStart(2,"0")}`}_durationDisplay(e){if(e==="offline")return _;let r=this._stateOf("session_duration"),n=r?.attributes?.duration_seconds;if(typeof n=="number"&&Number.isFinite(n)){let s=n;if(e==="charging"&&r?.last_updated){let o=(Date.now()-new Date(r.last_updated).getTime())/1e3;o>0&&o<15&&(s+=o)}return this._formatHMS(s)}return this._formatDuration(this._num("session_duration"))}_formatHMS(e){let r=Math.max(0,Math.floor(e)),n=Math.floor(r/3600),s=Math.floor(r%3600/60),o=r%60,a=s.toString().padStart(2,"0"),c=o.toString().padStart(2,"0");return n>0?`${n}:${a}:${c}`:`${s}:${c}`}_fmtKwh(e){return new Intl.NumberFormat(this._hass.locale.language,{maximumFractionDigits:1}).format(e)}_reducedMotion(){return typeof window<"u"&&typeof window.matchMedia=="function"&&window.matchMedia("(prefers-reduced-motion: reduce)").matches}_handleTap(){let e=this._entities.status??this._entities.power??this._entities.charger_online;e&&this.dispatchEvent(new CustomEvent("hass-more-info",{detail:{entityId:e},bubbles:!0,composed:!0}))}};M.styles=Xt,S([L()],M.prototype,"_config",2),S([L()],M.prototype,"_history",2),S([L()],M.prototype,"_price",2);customElements.get(G)||customElements.define(G,M);window.customCards=window.customCards??[];window.customCards.push({type:G,name:"Wellborne Charger Card",description:"Monitoring card for the Wellborne EV charger (live status, energy, cost).",preview:!0,documentationURL:"https://github.com/your/repo/tree/main/charger-card"});console.info(`%c WELLBORNE-CHARGER-CARD %c v${te} `,"background:#0f9d58;color:#fff","");export{M as WellborneChargerCard};
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
