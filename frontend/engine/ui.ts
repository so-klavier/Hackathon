import { gsap } from 'gsap';

class uiEngine {
    private uiElement: HTMLElement;
    private styleElement: HTMLElement;

    constructor(uiElement: HTMLElement, styleElement: HTMLElement) {
        this.uiElement = uiElement;
        this.styleElement = styleElement;
    }


    function move(this: any, x: number, y: number) {
        const tl = gsap.timeline();
        tl.to(this.uiElement, {x: x, y: y, duration: 0.5, ease: "power2.out"})
            .to(this.styleElement, {x: x, y: y, duration: 0.5, ease: "power2.out"}, "<");

    }
}