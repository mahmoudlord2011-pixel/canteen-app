
import {ReflexEvent,applyEventActions,isNotNullOrUndefined,isTrue,mergeSlotProps} from "$/utils/state"
import DebounceInput from "react-debounce-input"
import {StateContexts,addEvents} from "$/utils/context"
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {Badge as RadixThemesBadge,Box as RadixThemesBox,Button as RadixThemesButton,Flex as RadixThemesFlex,Heading as RadixThemesHeading,Separator as RadixThemesSeparator,Text as RadixThemesText,TextField as RadixThemesTextField} from "@radix-ui/themes"
import {jsx} from "@emotion/react"








export const Debounceinput_debounceinput_e692bdff29c2f97a04378287ad606b02_60462651 = /*#__PURE__*/ (() => {
const Debounceinput_debounceinput_e692bdff29c2f97a04378287ad606b02_60462651 = memo(({children, ...rest}) => {
    const on_change_5635fb7402fb559e72d17253a0d206a6 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.canteen_app___canteen_app____state.change_name", ({ ["name"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__canteen_app___canteen_app____state = useContext(StateContexts.reflex___state____state__canteen_app___canteen_app____state)



    return(
        jsx(DebounceInput,{...mergeSlotProps(rest, ({ debounceTimeout:300, element:RadixThemesTextField.Root, onChange:on_change_5635fb7402fb559e72d17253a0d206a6, placeholder:"\u0627\u0633\u0645 \u0627\u0644\u0637\u0627\u0644\u0628", value:(isNotNullOrUndefined(reflex___state____state__canteen_app___canteen_app____state.student_name_rx_state_) ? reflex___state____state__canteen_app___canteen_app____state.student_name_rx_state_ : "") }), "inputRef")},)
    )
});
Debounceinput_debounceinput_e692bdff29c2f97a04378287ad606b02_60462651.displayName = "DebounceInput";
return Debounceinput_debounceinput_e692bdff29c2f97a04378287ad606b02_60462651;
})();

export const Debounceinput_debounceinput_590ca0086627489490216735ce8ad2cc_60462651 = /*#__PURE__*/ (() => {
const Debounceinput_debounceinput_590ca0086627489490216735ce8ad2cc_60462651 = memo(({children, ...rest}) => {
    const on_change_c34913ce7515f29c0044af69f1725cc2 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.canteen_app___canteen_app____state.change_class", ({ ["cls"] : _e?.["target"]?.["value"] }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])
const reflex___state____state__canteen_app___canteen_app____state = useContext(StateContexts.reflex___state____state__canteen_app___canteen_app____state)



    return(
        jsx(DebounceInput,{...mergeSlotProps(rest, ({ debounceTimeout:300, element:RadixThemesTextField.Root, onChange:on_change_c34913ce7515f29c0044af69f1725cc2, placeholder:"\u0627\u0644\u0641\u0635\u0644 (\u0645\u062b\u0627\u0644: 10-A)", value:(isNotNullOrUndefined(reflex___state____state__canteen_app___canteen_app____state.student_class_rx_state_) ? reflex___state____state__canteen_app___canteen_app____state.student_class_rx_state_ : "") }), "inputRef")},)
    )
});
Debounceinput_debounceinput_590ca0086627489490216735ce8ad2cc_60462651.displayName = "DebounceInput";
return Debounceinput_debounceinput_590ca0086627489490216735ce8ad2cc_60462651;
})();

export const Button_button_9d730c5c50b9b4a5036fe6c0f8797a43_60462651 = /*#__PURE__*/ (() => {
const Button_button_9d730c5c50b9b4a5036fe6c0f8797a43_60462651 = memo(({children, ...rest}) => {
    const on_click_51e9c79fa2fa5e712a2c589c338a6d76 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.canteen_app___canteen_app____state.add_item", ({ ["name"] : "\u0633\u0646\u062f\u0648\u062a\u0634 \u0628\u0637\u0627\u0637\u0633", ["price"] : 20 }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ color:"green", onClick:on_click_51e9c79fa2fa5e712a2c589c338a6d76, size:"1" }))},children)
    )
});
Button_button_9d730c5c50b9b4a5036fe6c0f8797a43_60462651.displayName = "Button";
return Button_button_9d730c5c50b9b4a5036fe6c0f8797a43_60462651;
})();

export const Button_button_6131e9a12cd146222abd65f52d963cae_60462651 = /*#__PURE__*/ (() => {
const Button_button_6131e9a12cd146222abd65f52d963cae_60462651 = memo(({children, ...rest}) => {
    const on_click_00606fb4f86532f51a9752a9d6d3380a = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.canteen_app___canteen_app____state.remove_item", ({ ["name"] : "\u0633\u0646\u062f\u0648\u062a\u0634 \u0628\u0637\u0627\u0637\u0633", ["price"] : 20 }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ color:"red", onClick:on_click_00606fb4f86532f51a9752a9d6d3380a, size:"1" }))},children)
    )
});
Button_button_6131e9a12cd146222abd65f52d963cae_60462651.displayName = "Button";
return Button_button_6131e9a12cd146222abd65f52d963cae_60462651;
})();

export const Button_button_71c9f40aa6c3b6a7bc248f9c47fde89b_60462651 = /*#__PURE__*/ (() => {
const Button_button_71c9f40aa6c3b6a7bc248f9c47fde89b_60462651 = memo(({children, ...rest}) => {
    const on_click_037f9cbf6298e9d08a907720976a16a9 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.canteen_app___canteen_app____state.add_item", ({ ["name"] : "\u0628\u0627\u0643\u062a \u0628\u0637\u0627\u0637\u0633", ["price"] : 15 }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ color:"green", onClick:on_click_037f9cbf6298e9d08a907720976a16a9, size:"1" }))},children)
    )
});
Button_button_71c9f40aa6c3b6a7bc248f9c47fde89b_60462651.displayName = "Button";
return Button_button_71c9f40aa6c3b6a7bc248f9c47fde89b_60462651;
})();

export const Button_button_e02576629de646984083a233216aeeb5_60462651 = /*#__PURE__*/ (() => {
const Button_button_e02576629de646984083a233216aeeb5_60462651 = memo(({children, ...rest}) => {
    const on_click_2418fb641f746758a41d224ecdfb7c30 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.canteen_app___canteen_app____state.remove_item", ({ ["name"] : "\u0628\u0627\u0643\u062a \u0628\u0637\u0627\u0637\u0633", ["price"] : 15 }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ color:"red", onClick:on_click_2418fb641f746758a41d224ecdfb7c30, size:"1" }))},children)
    )
});
Button_button_e02576629de646984083a233216aeeb5_60462651.displayName = "Button";
return Button_button_e02576629de646984083a233216aeeb5_60462651;
})();

export const Button_button_3f5636ef17adb41fb201cd6fd534cc86_60462651 = /*#__PURE__*/ (() => {
const Button_button_3f5636ef17adb41fb201cd6fd534cc86_60462651 = memo(({children, ...rest}) => {
    const on_click_8d4d2fe83d3dd657caba21d4de1673f8 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.canteen_app___canteen_app____state.add_item", ({ ["name"] : "\u0639\u0635\u064a\u0631 \u0637\u0627\u0632\u062c", ["price"] : 20 }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ color:"green", onClick:on_click_8d4d2fe83d3dd657caba21d4de1673f8, size:"1" }))},children)
    )
});
Button_button_3f5636ef17adb41fb201cd6fd534cc86_60462651.displayName = "Button";
return Button_button_3f5636ef17adb41fb201cd6fd534cc86_60462651;
})();

export const Button_button_9e52eefa268389f08516b4b3eb2b6a0e_60462651 = /*#__PURE__*/ (() => {
const Button_button_9e52eefa268389f08516b4b3eb2b6a0e_60462651 = memo(({children, ...rest}) => {
    const on_click_93f98a006778d3ea0d687d5f946f2ca3 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.canteen_app___canteen_app____state.remove_item", ({ ["name"] : "\u0639\u0635\u064a\u0631 \u0637\u0627\u0632\u062c", ["price"] : 20 }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ color:"red", onClick:on_click_93f98a006778d3ea0d687d5f946f2ca3, size:"1" }))},children)
    )
});
Button_button_9e52eefa268389f08516b4b3eb2b6a0e_60462651.displayName = "Button";
return Button_button_9e52eefa268389f08516b4b3eb2b6a0e_60462651;
})();

export const Foreach_comp_6d1fbe6374dab1fbcae23fa17d114346_60462651 = /*#__PURE__*/ (() => {
const Foreach_comp_6d1fbe6374dab1fbcae23fa17d114346_60462651 = memo(({children}) => {
    const reflex___state____state__canteen_app___canteen_app____state = useContext(StateContexts.reflex___state____state__canteen_app___canteen_app____state)



    return(
        Array.prototype.map.call(reflex___state____state__canteen_app___canteen_app____state.cart_rx_state_ ?? [],((i_rx_state_,index_c4bda796664b1a3520213d76dc5d0750)=>(jsx(RadixThemesText,{as:"p",key:index_c4bda796664b1a3520213d76dc5d0750,size:"2"},("\u2022 "+i_rx_state_)))))
    )
});
Foreach_comp_6d1fbe6374dab1fbcae23fa17d114346_60462651.displayName = "Foreach";
return Foreach_comp_6d1fbe6374dab1fbcae23fa17d114346_60462651;
})();

export const Bare_comp_eb67216d1575933cd4ac5e4c69f5270f_60462651 = /*#__PURE__*/ (() => {
const Bare_comp_eb67216d1575933cd4ac5e4c69f5270f_60462651 = memo(({children}) => {
    const reflex___state____state__canteen_app___canteen_app____state = useContext(StateContexts.reflex___state____state__canteen_app___canteen_app____state)



    return(
        ("\u0627\u0644\u0625\u062c\u0645\u0627\u0644\u064a: "+reflex___state____state__canteen_app___canteen_app____state.total_price_rx_state_+" \u062c.\u0645")
    )
});
Bare_comp_eb67216d1575933cd4ac5e4c69f5270f_60462651.displayName = "Bare";
return Bare_comp_eb67216d1575933cd4ac5e4c69f5270f_60462651;
})();

export const Button_button_94fa63a7f0ad7557bd85927bc0829bd8_60462651 = /*#__PURE__*/ (() => {
const Button_button_94fa63a7f0ad7557bd85927bc0829bd8_60462651 = memo(({children, ...rest}) => {
    const on_click_a7bbc50c0796c24a3cd1a2b9ef8c91b1 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.canteen_app___canteen_app____state.send_order", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx(RadixThemesButton,{...mergeSlotProps(rest, ({ color:"orange", css:({ ["width"] : "100%" }), onClick:on_click_a7bbc50c0796c24a3cd1a2b9ef8c91b1, size:"3" }))},children)
    )
});
Button_button_94fa63a7f0ad7557bd85927bc0829bd8_60462651.displayName = "Button";
return Button_button_94fa63a7f0ad7557bd85927bc0829bd8_60462651;
})();

export const Foreach_comp_1f5ea28b0906597edaca8f9f31d958a2_60462651 = /*#__PURE__*/ (() => {
const Foreach_comp_1f5ea28b0906597edaca8f9f31d958a2_60462651 = memo(({children}) => {
    const reflex___state____state__canteen_app___canteen_app____state = useContext(StateContexts.reflex___state____state__canteen_app___canteen_app____state)



    return(
        Array.prototype.map.call(reflex___state____state__canteen_app___canteen_app____state.orders_rx_state_ ?? [],((order_rx_state_,index_189a9b834b41f94174732e17f0573f2f)=>(jsx(RadixThemesBox,{css:({ ["padding"] : "1em", ["border"] : "1px solid gray", ["borderRadius"] : "8px", ["width"] : "100%", ["backgroundColor"] : "rgba(255,255,255,0.05)" }),key:index_189a9b834b41f94174732e17f0573f2f},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",direction:"column",gap:"3"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",direction:"row",gap:"3"},jsx(RadixThemesBadge,{color:"purple",size:"2"},order_rx_state_?.["student_class"]),jsx(RadixThemesHeading,{size:"4"},order_rx_state_?.["student_name"]),jsx(RadixThemesFlex,{css:({ ["flex"] : 1, ["justifySelf"] : "stretch", ["alignSelf"] : "stretch" })},),jsx(RadixThemesText,{as:"p",css:({ ["color"] : "gray" }),size:"1"},order_rx_state_?.["time"])),jsx(RadixThemesSeparator,{size:"4"},),jsx(RadixThemesText,{as:"p",size:"2",weight:"bold"},("\u0627\u0644\u0623\u0635\u0646\u0627\u0641 \u0627\u0644\u0645\u0637\u0644\u0648\u0628\u0629: "+order_rx_state_?.["items_summary"])),jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",direction:"row",gap:"3"},jsx(RadixThemesText,{as:"p",css:({ ["color"] : "green" }),weight:"bold"},("\u0627\u0644\u0645\u0628\u0644\u063a: "+order_rx_state_?.["total_price"]+" \u062c.\u0645")),jsx(RadixThemesFlex,{css:({ ["flex"] : 1, ["justifySelf"] : "stretch", ["alignSelf"] : "stretch" })},),jsx(RadixThemesButton,{color:"green",onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.canteen_app___canteen_app____state.complete_order", ({ ["order"] : order_rx_state_ }), ({  })))], [_e], ({  })))),size:"1"},"\u0625\u062a\u0645\u0627\u0645 \u0648\u062a\u0642\u062f\u064a\u0645 \u0627\u0644\u0637\u0644\u0628 \u2705")))))))
    )
});
Foreach_comp_1f5ea28b0906597edaca8f9f31d958a2_60462651.displayName = "Foreach";
return Foreach_comp_1f5ea28b0906597edaca8f9f31d958a2_60462651;
})();

export const Cond_comp_d85a5aa3b5b85bcac4b5c17c965ebbaf_60462651 = /*#__PURE__*/ (() => {
const Cond_comp_d85a5aa3b5b85bcac4b5c17c965ebbaf_60462651 = memo(({children}) => {
    const reflex___state____state__canteen_app___canteen_app____state = useContext(StateContexts.reflex___state____state__canteen_app___canteen_app____state)



    return(
        ((reflex___state____state__canteen_app___canteen_app____state.orders_rx_state_.length?.valueOf?.() === 0?.valueOf?.())?(children?.at?.(0)):(children?.at?.(1)))
    )
});
Cond_comp_d85a5aa3b5b85bcac4b5c17c965ebbaf_60462651.displayName = "Cond";
return Cond_comp_d85a5aa3b5b85bcac4b5c17c965ebbaf_60462651;
})();
