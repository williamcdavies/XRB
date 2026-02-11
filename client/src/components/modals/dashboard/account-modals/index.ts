import ChangeEmailModal       from './ChangeEmailModal.vue'
import ChangeLanguageModal    from './ChangeLanguageModal.vue'
import ChangeNameModal        from './ChangeNameModal.vue'
import ChangePictureModal     from './ChangePictureModal.vue'
import ChangeAccountTypeModal from './ChangeAccountTypeModal.vue'
import DeleteAccountModal     from './DeleteAccountModal.vue'

export const accountModals = {
    email:    ChangeEmailModal,
    language: ChangeLanguageModal,
    name:     ChangeNameModal,
    picture:  ChangePictureModal,
    type:     ChangeAccountTypeModal,
    delete:   DeleteAccountModal
} as const

export type AccountModalType = keyof typeof accountModals