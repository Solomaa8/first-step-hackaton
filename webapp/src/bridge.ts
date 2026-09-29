/**
 * MAX Bridge / Mini App Bridge
 * Обеспечивает интеграцию мини-приложения с мессенджером MAX (window.WebApp)
 * и Telegram WebApp (window.Telegram.WebApp).
 */

declare global {
  interface Window {
    WebApp?: {
      ready?(): void;
      expand?(): void;
      close?(): void;
      sendData?(data: string): void;
      colorScheme?: "light" | "dark";
      themeParams?: Record<string, string>;
      platform?: string;
      version?: string;
      initData?: string;
      initDataUnsafe?: {
        user?: { id: number; first_name: string; last_name?: string; username?: string };
        chat?: { id: number; type: string };
      };
      HapticFeedback?: {
        impactOccurred(style: "light" | "medium" | "heavy"): void;
        notificationOccurred(type: "error" | "success" | "warning"): void;
        selectionChanged(): void;
      };
    };
    Telegram?: {
      WebApp?: any;
    };
  }
}

function getApp() {
  if (typeof window === "undefined") return null;
  return window.WebApp || window.Telegram?.WebApp || null;
}

export const bridge = {
  init() {
    const app = getApp();
    app?.ready?.();
    app?.expand?.();
  },

  getColorScheme(): "light" | "dark" {
    return getApp()?.colorScheme ?? "light";
  },

  getThemeParams(): Record<string, string> {
    return getApp()?.themeParams ?? {};
  },

  getUserId(): number {
    return getApp()?.initDataUnsafe?.user?.id ?? 12345;
  },

  getUserName(): string {
    const user = getApp()?.initDataUnsafe?.user;
    if (user?.first_name) {
      return user.last_name ? `${user.first_name} ${user.last_name}` : user.first_name;
    }
    return "Студент";
  },

  getPlatform(): string {
    return getApp()?.platform ?? "web";
  },

  hapticLight() {
    getApp()?.HapticFeedback?.impactOccurred?.("light");
  },

  hapticMedium() {
    getApp()?.HapticFeedback?.impactOccurred?.("medium");
  },

  hapticSuccess() {
    getApp()?.HapticFeedback?.notificationOccurred?.("success");
  },

  hapticSelectionChanged() {
    getApp()?.HapticFeedback?.selectionChanged?.();
  },

  sendDataToBot(data: object) {
    const json = JSON.stringify(data);
    getApp()?.sendData?.(json);
  },

  close() {
    getApp()?.close?.();
  },
};