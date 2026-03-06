declare namespace google.accounts.id {
    interface CredentialResponse {
        credential: string
        select_by: string
    }

    interface IdConfiguration {
        client_id: string
        callback: (response: CredentialResponse) => void
        auto_select?: boolean
        cancel_on_tap_outside?: boolean
    }

    function initialize(config: IdConfiguration): void
    function prompt(momentListener?: (notification: unknown) => void): void
}
