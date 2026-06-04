var St=Object.defineProperty;var fe=Object.getOwnPropertyDescriptor;var g=(r,t)=>()=>(r&&(t=r(r=0)),t);var me=(r,t)=>{for(var e in t)St(r,e,{get:t[e],enumerable:!0})};var S=(r,t,e,n)=>{for(var i=n>1?void 0:n?fe(t,e):t,s=r.length-1,o;s>=0;s--)(o=r[s])&&(i=(n?o(t,e,i):o(i))||i);return n&&i&&St(t,e,i),i};var J,Q,at,Ct,I,kt,D,Rt,ct,lt=g(()=>{J=globalThis,Q=J.ShadowRoot&&(J.ShadyCSS===void 0||J.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,at=Symbol(),Ct=new WeakMap,I=class{constructor(t,e,n){if(this._$cssResult$=!0,n!==at)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t,this.t=e}get styleSheet(){let t=this.o,e=this.t;if(Q&&t===void 0){let n=e!==void 0&&e.length===1;n&&(t=Ct.get(e)),t===void 0&&((this.o=t=new CSSStyleSheet).replaceSync(this.cssText),n&&Ct.set(e,t))}return t}toString(){return this.cssText}},kt=r=>new I(typeof r=="string"?r:r+"",void 0,at),D=(r,...t)=>{let e=r.length===1?r[0]:t.reduce((n,i,s)=>n+(o=>{if(o._$cssResult$===!0)return o.cssText;if(typeof o=="number")return o;throw Error("Value passed to 'css' function must be a 'css' function result: "+o+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(i)+r[s+1],r[0]);return new I(e,r,at)},Rt=(r,t)=>{if(Q)r.adoptedStyleSheets=t.map(e=>e instanceof CSSStyleSheet?e:e.styleSheet);else for(let e of t){let n=document.createElement("style"),i=J.litNonce;i!==void 0&&n.setAttribute("nonce",i),n.textContent=e.cssText,r.appendChild(n)}},ct=Q?r=>r:r=>r instanceof CSSStyleSheet?(t=>{let e="";for(let n of t.cssRules)e+=n.cssText;return kt(e)})(r):r});var ge,_e,ye,ve,be,$e,X,Tt,xe,we,z,W,tt,Pt,b,j=g(()=>{lt();lt();({is:ge,defineProperty:_e,getOwnPropertyDescriptor:ye,getOwnPropertyNames:ve,getOwnPropertySymbols:be,getPrototypeOf:$e}=Object),X=globalThis,Tt=X.trustedTypes,xe=Tt?Tt.emptyScript:"",we=X.reactiveElementPolyfillSupport,z=(r,t)=>r,W={toAttribute(r,t){switch(t){case Boolean:r=r?xe:null;break;case Object:case Array:r=r==null?r:JSON.stringify(r)}return r},fromAttribute(r,t){let e=r;switch(t){case Boolean:e=r!==null;break;case Number:e=r===null?null:Number(r);break;case Object:case Array:try{e=JSON.parse(r)}catch{e=null}}return e}},tt=(r,t)=>!ge(r,t),Pt={attribute:!0,type:String,converter:W,reflect:!1,useDefault:!1,hasChanged:tt};Symbol.metadata??=Symbol("metadata"),X.litPropertyMetadata??=new WeakMap;b=class extends HTMLElement{static addInitializer(t){this._$Ei(),(this.l??=[]).push(t)}static get observedAttributes(){return this.finalize(),this._$Eh&&[...this._$Eh.keys()]}static createProperty(t,e=Pt){if(e.state&&(e.attribute=!1),this._$Ei(),this.prototype.hasOwnProperty(t)&&((e=Object.create(e)).wrapped=!0),this.elementProperties.set(t,e),!e.noAccessor){let n=Symbol(),i=this.getPropertyDescriptor(t,n,e);i!==void 0&&_e(this.prototype,t,i)}}static getPropertyDescriptor(t,e,n){let{get:i,set:s}=ye(this.prototype,t)??{get(){return this[e]},set(o){this[e]=o}};return{get:i,set(o){let c=i?.call(this);s?.call(this,o),this.requestUpdate(t,c,n)},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)??Pt}static _$Ei(){if(this.hasOwnProperty(z("elementProperties")))return;let t=$e(this);t.finalize(),t.l!==void 0&&(this.l=[...t.l]),this.elementProperties=new Map(t.elementProperties)}static finalize(){if(this.hasOwnProperty(z("finalized")))return;if(this.finalized=!0,this._$Ei(),this.hasOwnProperty(z("properties"))){let e=this.properties,n=[...ve(e),...be(e)];for(let i of n)this.createProperty(i,e[i])}let t=this[Symbol.metadata];if(t!==null){let e=litPropertyMetadata.get(t);if(e!==void 0)for(let[n,i]of e)this.elementProperties.set(n,i)}this._$Eh=new Map;for(let[e,n]of this.elementProperties){let i=this._$Eu(e,n);i!==void 0&&this._$Eh.set(i,e)}this.elementStyles=this.finalizeStyles(this.styles)}static finalizeStyles(t){let e=[];if(Array.isArray(t)){let n=new Set(t.flat(1/0).reverse());for(let i of n)e.unshift(ct(i))}else t!==void 0&&e.push(ct(t));return e}static _$Eu(t,e){let n=e.attribute;return n===!1?void 0:typeof n=="string"?n:typeof t=="string"?t.toLowerCase():void 0}constructor(){super(),this._$Ep=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Em=null,this._$Ev()}_$Ev(){this._$ES=new Promise(t=>this.enableUpdating=t),this._$AL=new Map,this._$E_(),this.requestUpdate(),this.constructor.l?.forEach(t=>t(this))}addController(t){(this._$EO??=new Set).add(t),this.renderRoot!==void 0&&this.isConnected&&t.hostConnected?.()}removeController(t){this._$EO?.delete(t)}_$E_(){let t=new Map,e=this.constructor.elementProperties;for(let n of e.keys())this.hasOwnProperty(n)&&(t.set(n,this[n]),delete this[n]);t.size>0&&(this._$Ep=t)}createRenderRoot(){let t=this.shadowRoot??this.attachShadow(this.constructor.shadowRootOptions);return Rt(t,this.constructor.elementStyles),t}connectedCallback(){this.renderRoot??=this.createRenderRoot(),this.enableUpdating(!0),this._$EO?.forEach(t=>t.hostConnected?.())}enableUpdating(t){}disconnectedCallback(){this._$EO?.forEach(t=>t.hostDisconnected?.())}attributeChangedCallback(t,e,n){this._$AK(t,n)}_$ET(t,e){let n=this.constructor.elementProperties.get(t),i=this.constructor._$Eu(t,n);if(i!==void 0&&n.reflect===!0){let s=(n.converter?.toAttribute!==void 0?n.converter:W).toAttribute(e,n.type);this._$Em=t,s==null?this.removeAttribute(i):this.setAttribute(i,s),this._$Em=null}}_$AK(t,e){let n=this.constructor,i=n._$Eh.get(t);if(i!==void 0&&this._$Em!==i){let s=n.getPropertyOptions(i),o=typeof s.converter=="function"?{fromAttribute:s.converter}:s.converter?.fromAttribute!==void 0?s.converter:W;this._$Em=i;let c=o.fromAttribute(e,s.type);this[i]=c??this._$Ej?.get(i)??c,this._$Em=null}}requestUpdate(t,e,n,i=!1,s){if(t!==void 0){let o=this.constructor;if(i===!1&&(s=this[t]),n??=o.getPropertyOptions(t),!((n.hasChanged??tt)(s,e)||n.useDefault&&n.reflect&&s===this._$Ej?.get(t)&&!this.hasAttribute(o._$Eu(t,n))))return;this.C(t,e,n)}this.isUpdatePending===!1&&(this._$ES=this._$EP())}C(t,e,{useDefault:n,reflect:i,wrapped:s},o){n&&!(this._$Ej??=new Map).has(t)&&(this._$Ej.set(t,o??e??this[t]),s!==!0||o!==void 0)||(this._$AL.has(t)||(this.hasUpdated||n||(e=void 0),this._$AL.set(t,e)),i===!0&&this._$Em!==t&&(this._$Eq??=new Set).add(t))}async _$EP(){this.isUpdatePending=!0;try{await this._$ES}catch(e){Promise.reject(e)}let t=this.scheduleUpdate();return t!=null&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){if(!this.isUpdatePending)return;if(!this.hasUpdated){if(this.renderRoot??=this.createRenderRoot(),this._$Ep){for(let[i,s]of this._$Ep)this[i]=s;this._$Ep=void 0}let n=this.constructor.elementProperties;if(n.size>0)for(let[i,s]of n){let{wrapped:o}=s,c=this[i];o!==!0||this._$AL.has(i)||c===void 0||this.C(i,void 0,s,c)}}let t=!1,e=this._$AL;try{t=this.shouldUpdate(e),t?(this.willUpdate(e),this._$EO?.forEach(n=>n.hostUpdate?.()),this.update(e)):this._$EM()}catch(n){throw t=!1,this._$EM(),n}t&&this._$AE(e)}willUpdate(t){}_$AE(t){this._$EO?.forEach(e=>e.hostUpdated?.()),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t)}_$EM(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$ES}shouldUpdate(t){return!0}update(t){this._$Eq&&=this._$Eq.forEach(e=>this._$ET(e,this[e])),this._$EM()}updated(t){}firstUpdated(t){}};b.elementStyles=[],b.shadowRootOptions={mode:"open"},b[z("elementProperties")]=new Map,b[z("finalized")]=new Map,we?.({ReactiveElement:b}),(X.reactiveElementVersions??=[]).push("2.1.2")});function jt(r,t){if(!_t(r)||!r.hasOwnProperty("raw"))throw Error("invalid template strings array");return Mt!==void 0?Mt.createHTML(t):t}function M(r,t,e=r,n){if(t===T)return t;let i=n!==void 0?e._$Co?.[n]:e._$Cl,s=B(t)?void 0:t._$litDirective$;return i?.constructor!==s&&(i?._$AO?.(!1),s===void 0?i=void 0:(i=new s(r),i._$AT(r,e,n)),n!==void 0?(e._$Co??=[])[n]=i:e._$Cl=i),i!==void 0&&(t=M(r,i._$AS(r,t.values),i,n)),t}var gt,Ht,et,Mt,Dt,w,zt,Ae,R,K,B,_t,Ee,pt,F,Nt,Ot,C,Lt,Ut,Wt,yt,d,A,qe,T,p,It,k,Se,q,ht,G,N,ut,dt,ft,mt,Ce,Ft,nt=g(()=>{gt=globalThis,Ht=r=>r,et=gt.trustedTypes,Mt=et?et.createPolicy("lit-html",{createHTML:r=>r}):void 0,Dt="$lit$",w=`lit$${Math.random().toFixed(9).slice(2)}$`,zt="?"+w,Ae=`<${zt}>`,R=document,K=()=>R.createComment(""),B=r=>r===null||typeof r!="object"&&typeof r!="function",_t=Array.isArray,Ee=r=>_t(r)||typeof r?.[Symbol.iterator]=="function",pt=`[ 	
\f\r]`,F=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,Nt=/-->/g,Ot=/>/g,C=RegExp(`>|${pt}(?:([^\\s"'>=/]+)(${pt}*=${pt}*(?:[^ 	
\f\r"'\`<>=]|("|')|))|$)`,"g"),Lt=/'/g,Ut=/"/g,Wt=/^(?:script|style|textarea|title)$/i,yt=r=>(t,...e)=>({_$litType$:r,strings:t,values:e}),d=yt(1),A=yt(2),qe=yt(3),T=Symbol.for("lit-noChange"),p=Symbol.for("lit-nothing"),It=new WeakMap,k=R.createTreeWalker(R,129);Se=(r,t)=>{let e=r.length-1,n=[],i,s=t===2?"<svg>":t===3?"<math>":"",o=F;for(let c=0;c<e;c++){let a=r[c],l,u,h=-1,_=0;for(;_<a.length&&(o.lastIndex=_,u=o.exec(a),u!==null);)_=o.lastIndex,o===F?u[1]==="!--"?o=Nt:u[1]!==void 0?o=Ot:u[2]!==void 0?(Wt.test(u[2])&&(i=RegExp("</"+u[2],"g")),o=C):u[3]!==void 0&&(o=C):o===C?u[0]===">"?(o=i??F,h=-1):u[1]===void 0?h=-2:(h=o.lastIndex-u[2].length,l=u[1],o=u[3]===void 0?C:u[3]==='"'?Ut:Lt):o===Ut||o===Lt?o=C:o===Nt||o===Ot?o=F:(o=C,i=void 0);let m=o===C&&r[c+1].startsWith("/>")?" ":"";s+=o===F?a+Ae:h>=0?(n.push(l),a.slice(0,h)+Dt+a.slice(h)+w+m):a+w+(h===-2?c:m)}return[jt(r,s+(r[e]||"<?>")+(t===2?"</svg>":t===3?"</math>":"")),n]},q=class r{constructor({strings:t,_$litType$:e},n){let i;this.parts=[];let s=0,o=0,c=t.length-1,a=this.parts,[l,u]=Se(t,e);if(this.el=r.createElement(l,n),k.currentNode=this.el.content,e===2||e===3){let h=this.el.content.firstChild;h.replaceWith(...h.childNodes)}for(;(i=k.nextNode())!==null&&a.length<c;){if(i.nodeType===1){if(i.hasAttributes())for(let h of i.getAttributeNames())if(h.endsWith(Dt)){let _=u[o++],m=i.getAttribute(h).split(w),x=/([.?@])?(.*)/.exec(_);a.push({type:1,index:s,name:x[2],strings:m,ctor:x[1]==="."?ut:x[1]==="?"?dt:x[1]==="@"?ft:N}),i.removeAttribute(h)}else h.startsWith(w)&&(a.push({type:6,index:s}),i.removeAttribute(h));if(Wt.test(i.tagName)){let h=i.textContent.split(w),_=h.length-1;if(_>0){i.textContent=et?et.emptyScript:"";for(let m=0;m<_;m++)i.append(h[m],K()),k.nextNode(),a.push({type:2,index:++s});i.append(h[_],K())}}}else if(i.nodeType===8)if(i.data===zt)a.push({type:2,index:s});else{let h=-1;for(;(h=i.data.indexOf(w,h+1))!==-1;)a.push({type:7,index:s}),h+=w.length-1}s++}}static createElement(t,e){let n=R.createElement("template");return n.innerHTML=t,n}};ht=class{constructor(t,e){this._$AV=[],this._$AN=void 0,this._$AD=t,this._$AM=e}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(t){let{el:{content:e},parts:n}=this._$AD,i=(t?.creationScope??R).importNode(e,!0);k.currentNode=i;let s=k.nextNode(),o=0,c=0,a=n[0];for(;a!==void 0;){if(o===a.index){let l;a.type===2?l=new G(s,s.nextSibling,this,t):a.type===1?l=new a.ctor(s,a.name,a.strings,this,t):a.type===6&&(l=new mt(s,this,t)),this._$AV.push(l),a=n[++c]}o!==a?.index&&(s=k.nextNode(),o++)}return k.currentNode=R,i}p(t){let e=0;for(let n of this._$AV)n!==void 0&&(n.strings!==void 0?(n._$AI(t,n,e),e+=n.strings.length-2):n._$AI(t[e])),e++}},G=class r{get _$AU(){return this._$AM?._$AU??this._$Cv}constructor(t,e,n,i){this.type=2,this._$AH=p,this._$AN=void 0,this._$AA=t,this._$AB=e,this._$AM=n,this.options=i,this._$Cv=i?.isConnected??!0}get parentNode(){let t=this._$AA.parentNode,e=this._$AM;return e!==void 0&&t?.nodeType===11&&(t=e.parentNode),t}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(t,e=this){t=M(this,t,e),B(t)?t===p||t==null||t===""?(this._$AH!==p&&this._$AR(),this._$AH=p):t!==this._$AH&&t!==T&&this._(t):t._$litType$!==void 0?this.$(t):t.nodeType!==void 0?this.T(t):Ee(t)?this.k(t):this._(t)}O(t){return this._$AA.parentNode.insertBefore(t,this._$AB)}T(t){this._$AH!==t&&(this._$AR(),this._$AH=this.O(t))}_(t){this._$AH!==p&&B(this._$AH)?this._$AA.nextSibling.data=t:this.T(R.createTextNode(t)),this._$AH=t}$(t){let{values:e,_$litType$:n}=t,i=typeof n=="number"?this._$AC(t):(n.el===void 0&&(n.el=q.createElement(jt(n.h,n.h[0]),this.options)),n);if(this._$AH?._$AD===i)this._$AH.p(e);else{let s=new ht(i,this),o=s.u(this.options);s.p(e),this.T(o),this._$AH=s}}_$AC(t){let e=It.get(t.strings);return e===void 0&&It.set(t.strings,e=new q(t)),e}k(t){_t(this._$AH)||(this._$AH=[],this._$AR());let e=this._$AH,n,i=0;for(let s of t)i===e.length?e.push(n=new r(this.O(K()),this.O(K()),this,this.options)):n=e[i],n._$AI(s),i++;i<e.length&&(this._$AR(n&&n._$AB.nextSibling,i),e.length=i)}_$AR(t=this._$AA.nextSibling,e){for(this._$AP?.(!1,!0,e);t!==this._$AB;){let n=Ht(t).nextSibling;Ht(t).remove(),t=n}}setConnected(t){this._$AM===void 0&&(this._$Cv=t,this._$AP?.(t))}},N=class{get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}constructor(t,e,n,i,s){this.type=1,this._$AH=p,this._$AN=void 0,this.element=t,this.name=e,this._$AM=i,this.options=s,n.length>2||n[0]!==""||n[1]!==""?(this._$AH=Array(n.length-1).fill(new String),this.strings=n):this._$AH=p}_$AI(t,e=this,n,i){let s=this.strings,o=!1;if(s===void 0)t=M(this,t,e,0),o=!B(t)||t!==this._$AH&&t!==T,o&&(this._$AH=t);else{let c=t,a,l;for(t=s[0],a=0;a<s.length-1;a++)l=M(this,c[n+a],e,a),l===T&&(l=this._$AH[a]),o||=!B(l)||l!==this._$AH[a],l===p?t=p:t!==p&&(t+=(l??"")+s[a+1]),this._$AH[a]=l}o&&!i&&this.j(t)}j(t){t===p?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,t??"")}},ut=class extends N{constructor(){super(...arguments),this.type=3}j(t){this.element[this.name]=t===p?void 0:t}},dt=class extends N{constructor(){super(...arguments),this.type=4}j(t){this.element.toggleAttribute(this.name,!!t&&t!==p)}},ft=class extends N{constructor(t,e,n,i,s){super(t,e,n,i,s),this.type=5}_$AI(t,e=this){if((t=M(this,t,e,0)??p)===T)return;let n=this._$AH,i=t===p&&n!==p||t.capture!==n.capture||t.once!==n.once||t.passive!==n.passive,s=t!==p&&(n===p||i);i&&this.element.removeEventListener(this.name,this,n),s&&this.element.addEventListener(this.name,this,t),this._$AH=t}handleEvent(t){typeof this._$AH=="function"?this._$AH.call(this.options?.host??this.element,t):this._$AH.handleEvent(t)}},mt=class{constructor(t,e,n){this.element=t,this.type=6,this._$AN=void 0,this._$AM=e,this.options=n}get _$AU(){return this._$AM._$AU}_$AI(t){M(this,t)}},Ce=gt.litHtmlPolyfillSupport;Ce?.(q,G),(gt.litHtmlVersions??=[]).push("3.3.3");Ft=(r,t,e)=>{let n=e?.renderBefore??t,i=n._$litPart$;if(i===void 0){let s=e?.renderBefore??null;n._$litPart$=i=new G(t.insertBefore(K(),s),s,void 0,e??{})}return i._$AI(r),i}});var vt,v,ke,Kt=g(()=>{j();j();nt();nt();vt=globalThis,v=class extends b{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){let t=super.createRenderRoot();return this.renderOptions.renderBefore??=t.firstChild,t}update(t){let e=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Do=Ft(e,this.renderRoot,this.renderOptions)}connectedCallback(){super.connectedCallback(),this._$Do?.setConnected(!0)}disconnectedCallback(){super.disconnectedCallback(),this._$Do?.setConnected(!1)}render(){return T}};v._$litElement$=!0,v.finalized=!0,vt.litElementHydrateSupport?.({LitElement:v});ke=vt.litElementPolyfillSupport;ke?.({LitElement:v});(vt.litElementVersions??=[]).push("4.2.2")});var Bt=g(()=>{});var O=g(()=>{j();nt();Kt();Bt()});var qt=g(()=>{});function it(r){return(t,e)=>typeof e=="object"?Te(r,t,e):((n,i,s)=>{let o=i.hasOwnProperty(s);return i.constructor.createProperty(s,n),o?Object.getOwnPropertyDescriptor(i,s):void 0})(r,t,e)}var Re,Te,bt=g(()=>{j();Re={attribute:!0,type:String,converter:W,reflect:!1,hasChanged:tt},Te=(r=Re,t,e)=>{let{kind:n,metadata:i}=e,s=globalThis.litPropertyMetadata.get(i);if(s===void 0&&globalThis.litPropertyMetadata.set(i,s=new Map),n==="setter"&&((r=Object.create(r)).wrapped=!0),s.set(e.name,r),n==="accessor"){let{name:o}=e;return{set(c){let a=t.get.call(this);t.set.call(this,c),this.requestUpdate(o,a,r,!0,c)},init(c){return c!==void 0&&this.C(o,void 0,r,c),c}}}if(n==="setter"){let{name:o}=e;return function(c){let a=this[o];t.call(this,c),this.requestUpdate(o,a,r,!0,c)}}throw Error("Unsupported decorator location: "+n)}});function L(r){return it({...r,state:!0,attribute:!1})}var Gt=g(()=>{bt();});var Vt=g(()=>{});var U=g(()=>{});var Yt=g(()=>{U();});var Zt=g(()=>{U();});var Jt=g(()=>{U();});var Qt=g(()=>{U();});var Xt=g(()=>{U();});var $t=g(()=>{qt();bt();Gt();Vt();Yt();Zt();Jt();Qt();Xt()});var V,Y,ee,st,ot,ne,$,y,xt,Z=g(()=>{"use strict";V="wellborne-charger-card",Y="wellborne-charger-card-editor",ee="1.0.0",st="wellborne",ot={power:"power",energy:"energy",current:"current",max_current:"max_current",session_duration:"session_duration",status:"status",added_range:"added_range",monthly_energy:"monthly_energy",yearly_energy:"yearly_energy",last_session_energy:"last_session_energy",last_session_duration:"last_session_duration",session_cost:"session_cost",wifi_ssid:"wifi_ssid",charging:"charging",charger_online:"charger_online",vehicle_connected:"vehicle_connected"},ne=new Set(["charging","charger_online","vehicle_connected"]),$=new Set(["unavailable","unknown","none",""]),y="\u2014",xt={show_curve:!0,show_totals:!0,show_cost:!0,curve_hours:4}});var le={};me(le,{WellborneChargerCardEditor:()=>P});var Ie,P,At=g(()=>{"use strict";O();$t();Z();Ie=[{key:"show_curve",label:"Power curve (sparkline)"},{key:"show_totals",label:"Month / year totals"},{key:"show_cost",label:"Last-charge cost"}],P=class extends v{setConfig(t){this._config=t}render(){if(!this._config)return p;let t=this._config;return d`
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
            @input=${e=>{let n=e.target.value;this._set("price",n===""?void 0:Number(n))}}
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
                @change=${n=>this._set(e.key,n.target.checked)}
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
    `}_set(t,e){if(!this._config)return;let n={...this._config};e===void 0||e===""?delete n[t]:n[t]=e,this._config=n,this.dispatchEvent(new CustomEvent("config-changed",{detail:{config:n},bubbles:!0,composed:!0}))}};P.styles=D`
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
  `,S([it({attribute:!1})],P.prototype,"hass",2),S([L()],P.prototype,"_config",2);customElements.get(Y)||customElements.define(Y,P)});O();$t();O();var te=D`
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
  .last-when {
    font-size: 0.72rem;
    color: var(--wb-secondary);
    opacity: 0.85;
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
`;Z();Z();function re(r,t){let e={},n=Object.keys(ot);for(let s of n){let o=t[`${s}_entity`];typeof o=="string"&&o.length>0&&(e[s]=o)}if(!t.device)return e;let i=Pe(r,t.device);if(r.entities&&i){for(let s of Object.values(r.entities))if(s.device_id===t.device&&s.platform===st&&s.unique_id)for(let o of n)e[o]||s.unique_id===`${i}_${ot[o]}`&&(e[o]=s.entity_id)}if(r.entities)for(let s of Object.values(r.entities))s.device_id===t.device&&ie(e,n,s.entity_id,s.platform);if(!r.entities)for(let s of Object.keys(r.states))ie(e,n,s);return e}function Pe(r,t){let e=r.devices?.[t];if(e){for(let n of e.identifiers)if(n[0]===st)return n[1]}}function ie(r,t,e,n){let i=e.indexOf(".");if(i<0)return;let s=e.slice(0,i),o=e.slice(i+1);for(let c of t){if(r[c])continue;let l=ne.has(c)?"binary_sensor":"sensor";if(s!==l||n&&n!==st)continue;let u=ot[c];He(o,u)&&(r[c]=e)}}function He(r,t){if(!r.endsWith(`_${t}`))return!1;let e=r.slice(0,r.length-t.length-1);return!(t==="current"&&(e.endsWith("_max")||e.includes("household"))||t==="energy"&&e.endsWith("_last_session"))}Z();async function se(r,t){let e=Me(r,t.price_entity);if(e!==null)return{price:e,source:"CREG"};if(typeof t.price=="number"&&Number.isFinite(t.price)&&t.price>0)return{price:t.price,source:"static"};if(t.use_energy_prefs){let n=await Oe(r);if(n!==null)return{price:n,source:"energy-prefs"}}return null}function Me(r,t){if(!t)return null;let e=r.states[t];if(!e||$.has(e.state))return null;let n=Number(e.state);if(!Number.isFinite(n))return null;let i=String(e.attributes.unit_of_measurement??"").toLowerCase();return Ne(n,i)}function Ne(r,t){let e=t.replace(/\s+/g,"");return e.includes("/mwh")?r/1e3:e.includes("/wh")&&!e.includes("/kwh")?r*1e3:r}async function Oe(r){let t;try{t=await r.callWS({type:"energy/get_prefs"})}catch{return null}let n=t.energy_sources?.find(i=>i.type==="grid")?.flow_from?.[0];if(!n)return null;if(n.entity_energy_price){let i=r.states[n.entity_energy_price];if(i&&!$.has(i.state)){let s=Number(i.state);if(Number.isFinite(s))return s}}return typeof n.number_energy_price=="number"&&Number.isFinite(n.number_energy_price)?n.number_energy_price:null}function oe(r,t){return r===null||!Number.isFinite(r)?null:r*t}function wt(r,t,e){let n=t.currency??r.config.currency??"EUR";try{return new Intl.NumberFormat(r.locale.language,{style:"currency",currency:n}).format(e)}catch{return`${e.toFixed(2)} ${n}`}}O();function Le(r,t,e,n=2){let i=r.filter(f=>Number.isFinite(f.v));if(i.length===0)return{line:"",area:"",tip:null};if(i.length===1){let f=e/2;return{line:`M ${n} ${f} L ${t-n} ${f}`,area:`M ${n} ${f} L ${t-n} ${f} L ${t-n} ${e} L ${n} ${e} Z`,tip:{x:t-n,y:f}}}let s=i[0].t,c=i[i.length-1].t-s||1,a=-1/0,l=1/0;for(let f of i)f.v>a&&(a=f.v),f.v<l&&(l=f.v);l=Math.min(l,0);let u=a-l||1,h=t-n*2,_=e-n*2,m=i.map(f=>{let ue=n+(f.t-s)/c*h,de=n+_-(f.v-l)/u*_;return{x:ue,y:de}}),x=`M ${E(m[0].x)} ${E(m[0].y)}`;for(let f=1;f<m.length;f++)x+=` L ${E(m[f].x)} ${E(m[f].y)}`;let Et=m[m.length-1],pe=m[0],he=`${x} L ${E(Et.x)} ${E(e)} L ${E(pe.x)} ${E(e)} Z`;return{line:x,area:he,tip:Et}}function E(r){return(Math.round(r*100)/100).toString()}function ae(r,t){let{width:e,height:n,gradientId:i,animate:s,live:o}=t,c=Le(r,e,n);if(!c.line)return A`<svg viewBox="0 0 ${e} ${n}" width="100%" height="${n}" aria-hidden="true"></svg>`;let a=c.tip?A`
        <circle
          class="curve-tip ${o?"live":"static"} ${s?"animate":"noanim"}"
          cx="${c.tip.x}"
          cy="${c.tip.y}"
          r="2.6"
        ></circle>`:p;return A`
    <svg viewBox="0 0 ${e} ${n}" width="100%" height="${n}" preserveAspectRatio="none" aria-hidden="true">
      <defs>
        <linearGradient id="${i}" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="var(--wb-accent)" stop-opacity="0.18"></stop>
          <stop offset="100%" stop-color="var(--wb-accent)" stop-opacity="0"></stop>
        </linearGradient>
      </defs>
      <path class="curve-area" d="${c.area}" fill="url(#${i})"></path>
      <path class="curve-line" d="${c.line}" fill="none"></path>
      ${a}
    </svg>
  `}O();function ce(r){let t=r.size??96,e=8,n=(t-e)/2,i=t/2,s=t/2,o=2*Math.PI*n,c=Ue(r.percent,0,100),a=c/100*o,l=r.animate?"soc-arc animate":"soc-arc";return A`
    <svg viewBox="0 0 ${t} ${t}" width="${t}" height="${t}" class="soc-ring" role="img"
         aria-label="State of charge ${Math.round(c)} percent">
      <circle class="soc-track" cx="${i}" cy="${s}" r="${n}" fill="none" stroke-width="${e}"></circle>
      <circle
        class="${l}"
        cx="${i}"
        cy="${s}"
        r="${n}"
        fill="none"
        stroke-width="${e}"
        stroke-linecap="round"
        stroke-dasharray="${a} ${o-a}"
        transform="rotate(-90 ${i} ${s})"
      ></circle>
      <text class="soc-pct" x="${i}" y="${r.rangeLabel?s-2:s+1}" text-anchor="middle" dominant-baseline="middle">${Math.round(c)}%</text>
      ${r.rangeLabel?A`<text class="soc-range" x="${i}" y="${s+14}" text-anchor="middle" dominant-baseline="middle">${r.rangeLabel}</text>`:A``}
    </svg>
  `}function Ue(r,t,e){return Math.min(e,Math.max(t,r))}At();var De=220,ze=56,H=class extends v{constructor(){super(...arguments);this._history=[];this._price=null;this._entities={};this._lastHistoryFetch=0;this._historyKey="";this._priceKey=""}static async getConfigElement(){return await Promise.resolve().then(()=>(At(),le)),document.createElement(Y)}static getStubConfig(){return{type:`custom:${V}`,device:"",...xt}}getCardSize(){return 4}setConfig(e){if(!e)throw new Error("Invalid configuration");this._config={...xt,...e}}set hass(e){this._hass=e,this._config&&(this._entities=re(e,this._config),this._maybeFetchHistory(),this._maybeResolvePrice(),this.requestUpdate())}get hass(){return this._hass}connectedCallback(){super.connectedCallback(),this._tick=setInterval(()=>{if(!this._hass||!this._config||this._cardState()!=="charging")return;typeof this._stateOf("session_duration")?.attributes?.duration_seconds=="number"&&this.requestUpdate()},1e3)}disconnectedCallback(){super.disconnectedCallback(),this._tick&&(clearInterval(this._tick),this._tick=void 0)}_maybeResolvePrice(){if(!this._hass||!this._config.show_cost)return;let e=`${this._config.price_entity??""}|${this._config.price??""}|${this._config.use_energy_prefs??""}|${this._priceEntityState()}`;e!==this._priceKey&&(this._priceKey=e,se(this._hass,this._config).then(n=>{this._price=n}).catch(()=>{this._price=null}))}_priceEntityState(){let e=this._config.price_entity;return!e||!this._hass?"":this._hass.states[e]?.state??""}_maybeFetchHistory(){if(!this._hass||!this._config.show_curve)return;let e=this._entities.power;if(!e)return;let n=Date.now();if(!(e!==this._historyKey)&&n-this._lastHistoryFetch<25e3)return;this._historyKey=e,this._lastHistoryFetch=n;let s=this._config.curve_hours??4,o=new Date(n-s*36e5).toISOString(),c=`history/period/${encodeURIComponent(o)}?filter_entity_id=${encodeURIComponent(e)}&minimal_response&no_attributes`;this._hass.callApi("GET",c).then(a=>{this._history=this._parseHistory(a,e)}).catch(()=>{this._history=[]})}_parseHistory(e,n){let i=Array.isArray(e)?e.find(o=>o[0]?.entity_id===n)??e[0]:void 0;if(!i)return[];let s=[];for(let o of i){let c=Number(o.state);if(!Number.isFinite(c))continue;let a=o.last_changed??o.last_updated;s.push({t:a?Date.parse(a):Date.now(),v:c})}return s}_stateOf(e){let n=this._entities[e];if(!(!n||!this._hass))return this._hass.states[n]}_num(e){let n=this._stateOf(e);if(!n||$.has(n.state))return null;let i=Number(n.state);return Number.isFinite(i)?i:null}_str(e){let n=this._stateOf(e);return!n||$.has(n.state)?null:n.state}_bool(e){let n=this._stateOf(e);return!n||$.has(n.state)?null:n.state==="on"}_cardState(){if(this._bool("charger_online")===!1)return"offline";let n=this._bool("charging"),i=this._str("status");return n===!0||i==="charging"?"charging":"idle"}render(){if(!this._config||!this._hass)return p;let e=this._cardState(),n=this._config.name??this._hass.devices?.[this._config.device??""]?.name??"Wellborne Charger";return d`
      <ha-card @click=${this._handleTap}>
        <div class="card ${e}">
          ${this._renderHeader(n,e)}
          ${this._renderHero(e)}
          ${this._config.show_curve?this._renderCurveBlock(e):p}
          ${this._renderChips(e)}
          ${this._renderFooter()}
        </div>
      </ha-card>
    `}_renderHeader(e,n){let i=n!=="offline",s=n==="charging"?d`<span class="badge charging"><ha-icon icon="mdi:lightning-bolt"></ha-icon>Charging</span>`:n==="offline"?d`<span class="badge offline"><ha-icon icon="mdi:cloud-off-outline"></ha-icon>Offline</span>`:d`<span class="badge"><ha-icon icon="mdi:sleep"></ha-icon>Idle</span>`;return d`
      <div class="header">
        <div class="title">${e}</div>
        <div class="header-right">
          ${s}
          <span class="dot ${i?"online":"offline"}" title=${i?"online":"offline"}></span>
        </div>
      </div>
    `}_renderHero(e){let n=e==="offline",i=this._num("power"),s=n||i===null?y:(i/1e3).toFixed(1),o=this._durationDisplay(e);return d`
      <div class="hero">
        ${this._renderRing(e)}
        <div class="hero-main">
          <div class="live-row">
            <div class="kw">${s}<span class="unit">${s===y?"":"kW"}</span></div>
            <div class="duration">${o}</div>
          </div>
        </div>
      </div>
    `}_renderRing(e){let n=this._config.battery_entity;if(!n||!this._hass)return p;let i=this._hass.states[n];if(!i||$.has(i.state))return p;let s=Number(i.state);if(!Number.isFinite(s))return p;let o=this._rangeLabel(e);return d`
      <div class="ring-wrap">
        ${ce({percent:s,rangeLabel:o,animate:!this._reducedMotion()})}
      </div>
    `}_rangeLabel(e){if(e==="offline")return;let n=this._config.range_entity;if(n&&this._hass){let s=this._hass.states[n];if(s&&!$.has(s.state)&&Number.isFinite(Number(s.state)))return`${Math.round(Number(s.state))} km`}let i=this._num("added_range");return i===null?void 0:`+${Math.round(i)} km`}_renderCurveBlock(e){let n=e==="charging";return d`
      <div class="curve ${e}">
        <span class="curve-label">${n?"Live power":"Last session"}</span>
        ${ae(this._history,{width:De,height:ze,gradientId:"wb-curve-grad",animate:!this._reducedMotion(),live:n})}
      </div>
    `}_chip(e,n,i=!1){return d`<span class="chip ${i?"on":""}"><ha-icon icon=${e}></ha-icon>${n}</span>`}_renderChips(e){let n=e==="offline",i=this._bool("vehicle_connected"),s=n?null:this._num("current"),o=n?null:this._num("max_current"),c=s===null?y:o===null?`${s.toFixed(0)} A`:`${s.toFixed(0)} / ${o.toFixed(0)} A`,a=n?null:this._num("energy"),l=n?null:this._num("added_range"),u=n?null:this._num("session_cost"),h=i===!0?this._chip("mdi:power-plug","Connected",!0):this._chip("mdi:power-plug-outline",y);return d`
      <div class="chips">
        ${h} ${this._chip("mdi:current-ac",c)}
        ${this._chip("mdi:lightning-bolt",a===null?y:`${a.toFixed(1)} kWh`)}
        ${this._chip("mdi:map-marker-distance",l===null?y:`+${Math.round(l)} km`)}
        ${u===null||this._hass===void 0?p:this._chip("mdi:cash",wt(this._hass,this._config,u))}
      </div>
    `}_renderFooter(){let e=this._config.show_totals,n=this._config.show_cost;return!e&&!n?p:d`
      <div class="footer">
        ${e?this._renderTotals():p}
        ${n?this._renderLastCharge():p}
      </div>
    `}_renderTotals(){let e=this._num("monthly_energy"),n=this._num("yearly_energy");return d`
      <div class="stats">
        <div class="stat">
          <span class="stat-label">This month</span>
          <span class="stat-value">${e===null?y:`${this._fmtKwh(e)}`}<span class="stat-unit">kWh</span></span>
        </div>
        <div class="stat">
          <span class="stat-label">This year</span>
          <span class="stat-value">${n===null?y:`${this._fmtKwh(n)}`}<span class="stat-unit">kWh</span></span>
        </div>
      </div>
    `}_renderLastCharge(){let e=this._num("last_session_energy"),n=this._num("last_session_duration"),i=this._stateOf("last_session_energy")?.attributes,s=typeof i?.added_range=="number"?i.added_range:null,o=this._formatWhen(i?.end_time),a=[e===null?y:`${this._fmtKwh(e)} kWh`,this._formatDuration(n)];s!==null&&Number.isFinite(s)&&a.push(`+${Math.round(s)} km`);let l=a.join(" \xB7 "),u=d`
      <div class="last-info">
        <span class="last-label"><ha-icon icon="mdi:history"></ha-icon>Last charge</span>
        <span class="last-detail">${l}</span>
        ${o===null?p:d`<span class="last-when">${o}</span>`}
      </div>
    `,h=this._price===null?null:oe(e,this._price.price);if(h===null)return d`<div class="last">${u}</div>`;let _=wt(this._hass,this._config,h),m=this._price.source;return d`
      <div class="last">
        ${u}
        <div class="last-cost">
          <span class="last-cost-value">~${_}</span>
          <span class="last-cost-caption">est. · ${m}</span>
        </div>
      </div>
    `}_formatWhen(e){if(typeof e!="string"||e==="")return null;let n=new Date(e);return Number.isNaN(n.getTime())?null:new Intl.DateTimeFormat(this._hass.locale.language,{month:"short",day:"numeric",hour:"2-digit",minute:"2-digit"}).format(n)}_formatDuration(e){if(e===null||!Number.isFinite(e)||e<0)return y;let n=Math.floor(e/60),i=Math.round(e%60);return`${n}:${i.toString().padStart(2,"0")}`}_durationDisplay(e){if(e==="offline")return y;let n=this._stateOf("session_duration"),i=n?.attributes?.duration_seconds;if(typeof i=="number"&&Number.isFinite(i)){let s=i;if(e==="charging"&&n?.last_updated){let o=(Date.now()-new Date(n.last_updated).getTime())/1e3;o>0&&o<15&&(s+=o)}return this._formatHMS(s)}return this._formatDuration(this._num("session_duration"))}_formatHMS(e){let n=Math.max(0,Math.floor(e)),i=Math.floor(n/3600),s=Math.floor(n%3600/60),o=n%60,c=s.toString().padStart(2,"0"),a=o.toString().padStart(2,"0");return i>0?`${i}:${c}:${a}`:`${s}:${a}`}_fmtKwh(e){return new Intl.NumberFormat(this._hass.locale.language,{maximumFractionDigits:1}).format(e)}_reducedMotion(){return typeof window<"u"&&typeof window.matchMedia=="function"&&window.matchMedia("(prefers-reduced-motion: reduce)").matches}_handleTap(){let e=this._entities.status??this._entities.power??this._entities.charger_online;e&&this.dispatchEvent(new CustomEvent("hass-more-info",{detail:{entityId:e},bubbles:!0,composed:!0}))}};H.styles=te,S([L()],H.prototype,"_config",2),S([L()],H.prototype,"_history",2),S([L()],H.prototype,"_price",2);customElements.get(V)||customElements.define(V,H);window.customCards=window.customCards??[];window.customCards.push({type:V,name:"Wellborne Charger Card",description:"Monitoring card for the Wellborne EV charger (live status, energy, cost).",preview:!0,documentationURL:"https://github.com/your/repo/tree/main/charger-card"});console.info(`%c WELLBORNE-CHARGER-CARD %c v${ee} `,"background:#0f9d58;color:#fff","");export{H as WellborneChargerCard};
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
