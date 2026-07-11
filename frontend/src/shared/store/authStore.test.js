// @vitest-environment jsdom
import { beforeEach, describe, expect, it, vi } from "vitest";
import { useAuthStore } from "./authStore";
import { authApi } from "@/features/auth/api/authApi";

vi.mock("@/features/auth/api/authApi", () => ({
  authApi: {
    profile: vi.fn(),
  },
}));

describe("authStore", () => {
  beforeEach(() => {
    localStorage.clear();
    useAuthStore.setState({ user: null, isAuthenticated: false });
    vi.clearAllMocks();
  });

  it("clears auth state when a stored token is no longer valid", async () => {
    localStorage.setItem("access_token", "expired-token");
    authApi.profile.mockRejectedValueOnce(new Error("unauthorized"));

    await useAuthStore.getState().initializeAuth();

    expect(useAuthStore.getState().isAuthenticated).toBe(false);
    expect(useAuthStore.getState().user).toBeNull();
    expect(localStorage.getItem("access_token")).toBeNull();
    expect(localStorage.getItem("refresh_token")).toBeNull();
  });
});
