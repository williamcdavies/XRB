interface Api {
    fetch(input: RequestInfo, init?: RequestInit): Promise<Response>;
}

export interface GroupSummary {
    id: number;
    name: string;
    member_count: number;
}

export interface Member {
    id: number;
    email: string;
    first_name: string;
    last_name: string;
    role: 'admin' | 'user';
}

export interface GroupDetail {
    id: number;
    name: string;
    current_user_role: 'admin' | 'user';
    current_user_id: number;
    members: Member[];
}

export async function fetchGroups(api: Api): Promise<GroupSummary[]> {
    const res = await api.fetch('/api/groups/');
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Failed to load groups');
    return data.groups;
}

export async function fetchGroupDetail(api: Api, groupId: number): Promise<GroupDetail> {
    const res = await api.fetch(`/api/groups/${groupId}/`);
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Failed to load group');
    return data;
}

export async function createGroupRequest(api: Api, name: string): Promise<GroupDetail> {
    const res = await api.fetch('/api/groups/create/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Failed to create group');
    return data;
}

export async function addMemberRequest(api: Api, groupId: number, email: string): Promise<void> {
    const res = await api.fetch(`/api/groups/${groupId}/members/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Failed to add member');
}

export async function removeMemberRequest(api: Api, groupId: number, memberId: number): Promise<void> {
    const res = await api.fetch(
        `/api/groups/${groupId}/members/${memberId}/`,
        { method: 'DELETE' },
    );
    if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.error || 'Failed to remove member');
    }
}

export async function updateRoleRequest(api: Api, groupId: number, userId: number, role: 'admin' | 'user'): Promise<void> {
    const res = await api.fetch(
        `/api/groups/${groupId}/members/${userId}/role/`,
        {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ role }),
        },
    );
    if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.error || 'Failed to update role');
    }
}

export interface FilePermission {
    id: number;
    path: string;
    allowed_users: { id: number; email: string }[];
}

export async function fetchFilePermissions(api: Api, groupId: number): Promise<FilePermission[]> {
    const res = await api.fetch(`/api/groups/${groupId}/file-permissions/`);
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Failed to load file permissions');
    return data.permissions;
}

export async function setFilePermission(
    api: Api,
    groupId: number,
    path: string,
    allowedUserIds: number[],
): Promise<FilePermission> {
    const res = await api.fetch(`/api/groups/${groupId}/file-permissions/set/`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path, allowed_user_ids: allowedUserIds }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Failed to set file permission');
    return data;
}

export async function deleteFilePermission(api: Api, groupId: number, path: string): Promise<void> {
    const res = await api.fetch(
        `/api/groups/${groupId}/file-permissions/delete/?path=${encodeURIComponent(path)}`,
        { method: 'DELETE' },
    );
    if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.error || 'Failed to delete file permission');
    }
}

export async function deleteGroupRequest(api: Api, groupId: number): Promise<void> {
    const res = await api.fetch(
        `/api/groups/${groupId}/delete/`,
        { method: 'DELETE' },
    );
    if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.error || 'Failed to delete group');
    }
}
